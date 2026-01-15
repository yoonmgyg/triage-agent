import httpx
import json
import time

CONTROLLER_URL = "http://localhost:8010"

def trigger_evaluation():
    try:
        response = httpx.get(f"{CONTROLLER_URL}/agents")
        if response.status_code != 200:
            print(f"Error listing agents: {response.status_code}")
            return
        
        agents = response.json()
        green_id = None
        white_id = None
        
        for agent_id, info in agents.items():
            if info.get("state") == "running":
                if agent_id.startswith("green_"):
                    green_id = agent_id
                elif agent_id.startswith("white_"):
                    white_id = agent_id
        
        if not green_id or not white_id:
            print("Missing required agents (Green/White)")
            return
        
        print("Starting evaluation task...")
        task_data = {
            "task_id": f"eval_{int(time.time())}",
            "config": {"benchmark": "healthcare_triage"},
            "participants": {"agent": white_id}
        }
        
        task_url = f"{CONTROLLER_URL}/to_agent/{green_id}/handle_task"
        with httpx.Client(timeout=180.0) as client:
            resp = client.post(task_url, json=task_data)
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"Task Complete: {result.get('task_id')}")
            for artifact in result.get("artifacts", []):
                if artifact["name"] == "results.json":
                    content = json.loads(artifact["content"])
                    res = content.get("results", [{}])[0]
                    print(f"Pass Rate: {res.get('pass_rate', 0)*100:.1f}%")
                    print(f"Time: {res.get('time_used', 0):.2f}s")
        else:
            print(f"Task failed: {resp.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    trigger_evaluation()
