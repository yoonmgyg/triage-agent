from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ToolCall:
    tool_name: str
    request: Dict[str, Any]
    response: Dict[str, Any]


@dataclass
class SimulationTrace:
    scenario_id: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    agent_response: str | None = None


class HealthcareSimulationEnvironment:
    """
    Thin wrapper that white agent can use to call MCP tools
    """

    def __init__(self) -> None:
        self._trace = None

    def start(self, scenario_id: str) -> None:
        self._trace = SimulationTrace(scenario_id=scenario_id)

    @property
    def trace(self) -> SimulationTrace:
        if self._trace is None:
            raise RuntimeError("Simulation not started")
        return self._trace

    def record_tool_call(self, tool_name: str, request: Dict[str, Any], response: Dict[str, Any]) -> None:
        self.trace.tool_calls.append(
            ToolCall(tool_name=tool_name, request=request, response=response)
        )

    def set_agent_response(self, text: str) -> None:
        self.trace.agent_response = text
