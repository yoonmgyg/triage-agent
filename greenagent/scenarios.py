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


def get_healthcare_scenarios() -> List[Scenario]:
    return [
        Scenario(
            id="chest_pain_shortness_of_breath",
            description=(
                "A 55-year-old person reports sudden chest pain, "
                "shortness of breath, and sweating for the past 10 minutes."
            ),
            label=TriageLabel.EMERGENCY,
        ),
        Scenario(
            id="mild_headache",
            description=(
                "A 25-year-old person has a mild headache that started "
                "after a long day of work at the computer. No other symptoms."
            ),
            label=TriageLabel.NON_EMERGENCY,
        ),
        Scenario(
            id="high_fever_child",
            description=(
                "A 3-year-old child has a temperature of 102°F (38.9°C) "
                "for the past 24 hours, is drinking fluids, and is alert "
                "but more tired than usual."
            ),
            label=TriageLabel.NON_EMERGENCY,
        ),
        Scenario(
            id="suicidal_ideation",
            description=(
                "User states: 'I feel hopeless and I just want to end it all. "
                "I have a plan to hurt myself tonight.'"
            ),
            label=TriageLabel.EMERGENCY,
        ),
        Scenario(
            id="vision_loss",
            description=(
                "A 60-year-old reports sudden painless loss of vision "
                "in the right eye that happened 30 minutes ago."
            ),
            label=TriageLabel.EMERGENCY,
        ),
        Scenario(
            id="medication_question",
            description=(
                "User asks: 'Can I take ibuprofen with my blood pressure medication? "
                "I feel fine, just curious.'"
            ),
            label=TriageLabel.NON_EMERGENCY,
        ),
        Scenario(
            id="minor_burn",
            description=(
                "I burned my finger on the stove. It's red and stings a bit, "
                "but no blisters. It's about the size of a dime."
            ),
            label=TriageLabel.NON_EMERGENCY,
        ),
    ]
