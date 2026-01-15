from typing import Dict, Any

from healthcare_data import list_patients
from simulation_env import HealthcareSimulationEnvironment
from scenarios import get_healthcare_scenarios
from purpleagent import HealthcareTriageAgent
from evaluator_logic import HealthcareTriageEvaluator


def run_single_eval() -> Dict[str, Any]:
    """
    Runs one evaluation over all scenarios using the green evaluator
    and purple agent, printing results and returning the raw payload.
    """

    purple_agent = HealthcareTriageAgent()

    class LocalA2AClient:
        def call_agent(self, agent_id: str, messages):
            from purpleagent import TaskRequest, TaskResult, Message

            request = TaskRequest(
                task_id="local_task",
                config={},
                messages=messages,
            )
            result: TaskResult = purple_agent.handle_task(request)
            if not result.messages:
                return ""
            return result.messages[-1].content

    a2a_client = LocalA2AClient()
    evaluator = HealthcareTriageEvaluator(a2a_client=a2a_client)

    # create a dummy TaskRequest for the green evaluator
    from greenagent import TaskRequest as GreenTaskRequest

    request = GreenTaskRequest(
        task_id="eval_run_001",
        config={},
        participants={"agent": "local_purple_agent"},
    )

    # run the evaluation
    result = evaluator.handle_task(request)

    # print human friendly output
    print("Evaluation completed")
    for artifact in result.artifacts:
        if artifact.name == "results.json":
            print("results.json:")
            print(artifact.content)

    return {
        "artifacts": [
            {
                "name": artifact.name,
                "mime_type": artifact.mime_type,
                "content": artifact.content,
            }
            for artifact in result.artifacts
        ]
    }


if __name__ == "__main__":
    run_single_eval()
