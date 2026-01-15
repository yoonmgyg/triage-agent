import httpx
import json
import asyncio
from uuid import uuid4
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Role, Part, TextPart, Task

async def verify_benchmark():
    evaluator_url = "http://localhost:9010"
    participant_url = "http://participant:9009"

    print("Starting End-to-End Verification...")
    
    async with httpx.AsyncClient(timeout=30.0) as httpx_client:
        # 1. Resolve Evaluator Card
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=evaluator_url)
        try:
            agent_card = await resolver.get_agent_card()
            # OVERRIDE: Point the SDK to the host-mapped port for message sending
            agent_card.url = evaluator_url
            print(f"Evaluator reachable: {agent_card.name}")
        except Exception as e:
            print(f"Evaluator not reachable: {e}")
            return

        # 2. Setup A2A Client
        config = ClientConfig(httpx_client=httpx_client)
        factory = ClientFactory(config)
        client = factory.create(agent_card)

        # 3. Create Evaluation Message
        msg = Message(
            kind="message",
            role=Role.user,
            parts=[Part(root=TextPart(kind="text", text=json.dumps({
                "participants": {"agent": participant_url},
                "config": {"benchmark": "healthcare_triage"}
            })))],
            message_id=uuid4().hex,
        )

        print("Sending evaluation request via A2A SDK...")
        
        task_id = None
        
        # 4. Send Message and look for Task
        async for event in client.send_message(msg):
            # The SDK returns events which can be Message or (Task, Update)
            if isinstance(event, tuple):
                task_obj, update = event
                if isinstance(task_obj, Task):
                    task_id = task_obj.id
                    print(f"Task {task_id} created. Monitoring...")
                    break
            elif isinstance(event, Task):
                task_id = event.id
                print(f"Task {task_id} created. Monitoring...")
                break

        if not task_id:
            print("No task was created by the evaluator.")
            return

        # 5. Monitor Task until terminal state
        while True:
            # The SDK expects TaskQueryParams with 'id' field
            task_status = await client.get_task({"id": task_id})
            state = task_status.status.state.value
            
            if state in ["completed", "failed", "rejected"]:
                print(f"Task finished with state: {state}")
                if state == "completed":
                    # Look for results.json in artifacts
                    for artifact in task_status.artifacts:
                        if artifact.name == "results.json":
                            # Find the DataPart in the parts list
                            res = None
                            for part in artifact.parts:
                                if hasattr(part.root, "data"):
                                    data = part.root.data
                                    # Handle flat dict, new list, and old dict format for robust backward compatibility
                                    if isinstance(data, list):
                                        res = data[0]
                                    elif "results" in data and isinstance(data["results"], list):
                                        res = data["results"][0]
                                    else:
                                        res = data
                                    break
                            
                            if res:
                                print(f"\nASSESSMENT COMPLETE")
                                print(f"----------------------")
                                print(f"Pass Rate: {res['accuracy']*100:.1f}%")
                                print(f"Score: {res['score']}/{res['max_score']}")
                                print(f"Time: {res['time_used']:.2f}s")
                                
                                if "per_scenario" in res:
                                    print(f"\nFAILURES:")
                                    for s in res["per_scenario"]:
                                        if s["score"] < 1:
                                            print(f"- {s['scenario_id']}: {s['reasons']}")
                                return
                            else:
                                print("Results file found but no DataPart was detected.")
                    print("Task completed but no results.json artifact was found.")
                else:
                    print(f"Task failed or was rejected: {task_status.status.message}")
                break
            
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(verify_benchmark())
