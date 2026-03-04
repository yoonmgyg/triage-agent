from dataclasses import dataclass
from enum import Enum
from typing import List


class TriageLabel(str, Enum):
    EMERGENCY = "emergency"
    NON_EMERGENCY = "non_emergency"


@dataclass
class Scenario:
    id: str
    description: str
    label: TriageLabel


import json
from pathlib import Path

def get_healthcare_scenarios() -> List[Scenario]:
    json_path = Path(__file__).parent / "scenarios.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Scenario(id=item["id"], description=item["description"], label=TriageLabel(item["label"])) for item in data]
