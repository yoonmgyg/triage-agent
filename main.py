import os
import uvicorn
import json
import time
import httpx
from fastapi import FastAPI
from evaluator_logic import HealthcareTriageEvaluator, TaskRequest as GreenTaskRequest

class AgentBeatsA2AClient:
    def __init__(self, controller_url="http://localhost:8010"):
        self.controller_url = controller_url

    def call_agent(self, agent_id, messages):
        if agent_id == "simulated-agent":
            return "Simulated response"

        payload = [{"role": m.role, "content": m.content} for m in messages]
        proxy_url = f"{self.controller_url}/to_agent/{agent_id}/handle_message"
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(proxy_url, json={"messages": payload})
                if response.status_code == 200:
                    return response.json().get("content", "")
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Failed: {e}"

class AgentBeatsWrapper:
    def __init__(self):
        self.evaluator = HealthcareTriageEvaluator(a2a_client=AgentBeatsA2AClient())

    def handle_task(self, task_id, config, participants):
        request = GreenTaskRequest(
            task_id=task_id,
            config=config,
            participants=participants
        )
        return self.evaluator.handle_task(request)

app = FastAPI(title="Green Agent")
wrapper = AgentBeatsWrapper()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/.well-known/agent-card.json")
def get_agent_card():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("AGENT_PORT", "8001"))
    agent_url = os.environ.get("AGENT_URL", f"http://{host}:{port}")
    
    return {
        "name": "HealthcareTriageGreenAgent",
        "version": "1.0.0",
        "description": "Evaluator agent for healthcare triage",
        "url": agent_url,
        "capabilities": {
            "extensions": [],
            "pushNotifications": False,
            "streaming": False,
            "stateTransitionHistory": False
        },
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "skills": [
            {
                "id": "evaluate-triage",
                "name": "Healthcare Triage Evaluator",
                "description": "Evaluates healthcare triage performance",
                "tags": ["healthcare", "triage", "evaluation"]
            }
        ]
    }

@app.post("/handle_task")
async def handle_task(request: dict):
    task_id = request.get("task_id") or request.get("id") or f"task_{int(time.time())}"
    config = request.get("config", {})
    participants = request.get("participants", {})
    
    result = wrapper.handle_task(task_id, config, participants)
    
    webhook_url = os.environ.get("WEBHOOK_URL")
    if webhook_url:
        try:
            report_payload = next((json.loads(a.content) for a in result.artifacts if a.name == "results.json"), None)
            if report_payload:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.post(webhook_url, json=report_payload)
        except Exception as e:
            print(f"Webhook error: {e}")
    
    return {
        "task_id": result.task_id,
        "artifacts": [
            {
                "name": a.name,
                "mime_type": a.mime_type,
                "content": a.content
            } for a in result.artifacts
        ]
    }

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("AGENT_PORT", "8001"))
    uvicorn.run(app, host=host, port=port)
