import os
import uvicorn
from fastapi import FastAPI
from purpleagent import HealthcareTriageAgent, Message

app = FastAPI(title="White Agent")
agent = HealthcareTriageAgent()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/.well-known/agent-card.json")
def get_agent_card():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("AGENT_PORT", "8002"))
    agent_url = os.environ.get("AGENT_URL", f"http://{host}:{port}")
    
    return {
        "name": "HealthcareTriageWhiteAgent",
        "version": "1.0.0",
        "description": "Baseline participant agent for healthcare triage",
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
                "id": "triage-healthcare",
                "name": "Healthcare Triage",
                "description": "Categorizes healthcare symptoms",
                "tags": ["healthcare", "triage"]
            }
        ]
    }

@app.post("/handle_message")
async def handle_message(request: dict):
    messages = [Message(**m) for m in request.get("messages", [])]
    # The baseline agent expects a single message or a list; here we process the latest
    if not messages:
        return {"content": "No message received."}
    
    # Simplification for baseline A2A wrap
    response = agent.build_reply(messages)
    return {"content": response}

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("AGENT_PORT", "8002"))
    uvicorn.run(app, host=host, port=port)
