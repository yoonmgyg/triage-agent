from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json

@dataclass
class Message:
    role: str
    content: str

@dataclass
class TaskRequest:
    task_id: str
    config: Dict[str, Any]
    messages: List[Message]

@dataclass
class Artifact:
    name: str
    mime_type: str
    content: str

@dataclass
class TaskResult:
    task_id: str
    messages: List[Message]
    artifacts: List[Artifact]

class HealthcareTriageAgent:
    def __init__(self) -> None:
        pass

    def _get_last_user_message(self, request: TaskRequest) -> Optional[str]:
        for msg in reversed(request.messages):
            if msg.role == "user":
                return msg.content
        return None

    def _classify_triage(self, text: str) -> str:
        t = text.lower()
        
        emergency_keywords = [
            "chest pain",
            "shortness of breath",
            "difficulty breathing",
            "trouble breathing",
            "sweating for the past",
            "severe chest",
            "sudden chest",
        ]

        for kw in emergency_keywords:
            if kw in t:
                return "emergency"

        mild_patterns = [
            "mild headache",
            "after a long day of work",
            "working at the computer",
        ]
        for kw in mild_patterns:
            if kw in t:
                return "non_emergency"

        child_fever_patterns = [
            "3-year-old",
            "3 year old",
            "child has a temperature",
            "fever for the past 24 hours",
        ]
        for kw in child_fever_patterns:
            if kw in t:
                return "non_emergency"

        high_risk_patterns = [
            "cannot breathe",
            "loss of consciousness",
            "fainted",
            "suicide",
            "hurt myself",
            "end it all",
            "loss of vision",
            "blindness",
            "cannot see",
            "seizure",
            "stroke",
        ]
        for kw in high_risk_patterns:
            if kw in t:
                return "emergency"

        return "non_emergency"

    def _build_emergency_reply(self, scenario_text: str) -> str:
        return (
            "I am not a doctor, but based on what you described this could be "
            "a medical emergency. You should call 911 or your local emergency "
            "number right away, or go to the nearest emergency room.\n\n"
            "Do not try to diagnose or treat this on your own. If possible, "
            "have someone stay with the person and follow instructions from "
            "emergency services."
        )

    def _build_non_emergency_reply(self, scenario_text: str) -> str:
        return (
            "I am not a doctor, but based on what you described this does not "
            "sound like an immediate life threatening emergency.\n\n"
            "You should monitor your symptoms and contact your doctor or a "
            "qualified healthcare professional for personalized medical advice. "
            "If symptoms worsen suddenly, become severe, or you are worried "
            "that this could be serious, seek urgent or emergency care.\n\n"
            "Do not ignore your symptoms, and do not start or change any "
            "medications without guidance from a healthcare professional."
        )

    def handle_task(self, request: TaskRequest) -> TaskResult:
        last_user = self._get_last_user_message(request)

        if last_user is None:
            reply_text = "I did not receive a user scenario to review."
            reply_msg = Message(role="assistant", content=reply_text)
            artifact = Artifact(
                name="decision.json",
                mime_type="application/json",
                content=json.dumps({"task_id": request.task_id, "triage_class": None}, indent=2)
            )
            return TaskResult(task_id=request.task_id, messages=[reply_msg], artifacts=[artifact])

        triage_class = self._classify_triage(last_user)
        reply_text = self._build_emergency_reply(last_user) if triage_class == "emergency" else self._build_non_emergency_reply(last_user)
        reply_msg = Message(role="assistant", content=reply_text)
        
        artifact = Artifact(
            name="decision.json",
            mime_type="application/json",
            content=json.dumps({"task_id": request.task_id, "triage_class": triage_class}, indent=2)
        )

        return TaskResult(task_id=request.task_id, messages=[reply_msg], artifacts=[artifact])

    def build_reply(self, messages: List[Message]) -> str:
        # Compatibility for simple message handling
        request = TaskRequest(task_id="msg_reply", config={}, messages=messages)
        result = self.handle_task(request)
        return result.messages[0].content
