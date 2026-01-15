import httpx
import json
import time
import asyncio

async def verify_benchmark():
    evaluator_url = "http://localhost:9010"
    participant_url = "http://participant:9009" # URL inside the docker network

    print("🚀 Starting End-to-End Verification...")
    
    # 1. Check if Evaluator is up
    try:
        resp = httpx.get(f"{evaluator_url}/.well-known/agent-card.json")
        print(f"✅ Evaluator reachable: {resp.json().get('name')}")
    except Exception as e:
        print(f"❌ Evaluator not reachable: {e}")
        return

    # 2. Trigger Triage Task
    task_payload = {
        "kind": "message",
        "role": "user",
        "parts": [{"kind": "text", "text": json.dumps({
            "participants": {"agent": participant_url},
            "config": {"benchmark": "healthcare_triage"}
        })}],
        "message_id": "test_verification"
    }

    print("📤 Sending evaluation request to Green Agent...")
    async with httpx.AsyncClient(timeout=300.0) as client:
        resp = await client.post(f"{evaluator_url}/tasks", json=task_payload)
        if resp.status_code != 201:
            print(f"❌ Failed to create task: {resp.text}")
            return
        
        task_id = resp.json().get("id")
        print(f"⏳ Task {task_id} running...")

        # 3. Poll for Completion
        while True:
            t_resp = await client.get(f"{evaluator_url}/tasks/{task_id}")
            task_status = t_resp.json()
            state = task_status.get("status", {}).get("state")
            
            if state in ["completed", "failed", "rejected"]:
                print(f"🏁 Task finished with state: {state}")
                if state == "completed":
                    # Find results.json artifact
                    for artifact in task_status.get("artifacts", []):
                        if artifact["name"] == "results.json":
                            results = artifact["parts"][0]["root"]["data"]
                            res = results["results"][0]
                            print(f"\n🏆 ASSESSMENT COMPLETE")
                            print(f"----------------------")
                            print(f"Pass Rate: {res['accuracy']*100:.1f}%")
                            print(f"Score: {res['score']}/{res['max_score']}")
                            print(f"Time: {res['time_used']:.2f}s")
                            break
                break
            
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(verify_benchmark())
