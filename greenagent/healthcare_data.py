from typing import Dict, Any, List


PatientRecord = Dict[str, Any]


PATIENTS: Dict[str, PatientRecord] = {
    "patient_001": {
        "id": "patient_001",
        "name": "Patient 001",
        "age": 55,
        "sex": "male",
        "vitals": {
            "heart_rate": 96,
            "blood_pressure": "145/92",
            "resp_rate": 20,
            "temperature_c": 37.2,
        },
        "problems": [
            "hypertension",
            "hyperlipidemia",
        ],
        "medications": [
            {"name": "atorvastatin", "dose": "20 mg", "frequency": "once daily"},
            {"name": "lisinopril", "dose": "10 mg", "frequency": "once daily"},
        ],
        "recent_encounters": [
            {
                "date": "2025-10-10",
                "summary": "Follow up for blood pressure control, no acute complaints.",
            }
        ],
    },
    "patient_002": {
        "id": "patient_002",
        "name": "Patient 002",
        "age": 25,
        "sex": "female",
        "vitals": {
            "heart_rate": 78,
            "blood_pressure": "118/76",
            "resp_rate": 16,
            "temperature_c": 36.8,
        },
        "problems": [
            "episodic tension headache",
        ],
        "medications": [],
        "recent_encounters": [
            {
                "date": "2025-09-12",
                "summary": "Evaluated for headaches, advised ergonomic changes and breaks.",
            }
        ],
    },
    "patient_003": {
        "id": "patient_003",
        "name": "Patient 003",
        "age": 3,
        "sex": "female",
        "vitals": {
            "heart_rate": 110,
            "blood_pressure": "not recorded",
            "resp_rate": 24,
            "temperature_c": 38.9,
        },
        "problems": [
            "recurrent upper respiratory infections",
        ],
        "medications": [],
        "recent_encounters": [
            {
                "date": "2025-11-01",
                "summary": "Seen for cough and congestion, viral illness suspected.",
            }
        ],
    },
    "patient_004": {
        "id": "patient_004",
        "name": "Patient 004",
        "age": 67,
        "sex": "female",
        "vitals": {
            "heart_rate": 84,
            "blood_pressure": "132/80",
            "resp_rate": 18,
            "temperature_c": 36.9,
        },
        "problems": [
            "type 2 diabetes",
            "osteoarthritis",
        ],
        "medications": [
            {"name": "metformin", "dose": "500 mg", "frequency": "twice daily"},
        ],
        "recent_encounters": [
            {
                "date": "2025-10-28",
                "summary": "Routine diabetes follow up. A1c 7.3%",
            }
        ],
    },
    "patient_005": {
        "id": "patient_005",
        "name": "Patient 005",
        "age": 42,
        "sex": "male",
        "vitals": {
            "heart_rate": 72,
            "blood_pressure": "124/78",
            "resp_rate": 16,
            "temperature_c": 36.7,
        },
        "problems": [
            "mild intermittent asthma",
        ],
        "medications": [
            {"name": "albuterol inhaler", "dose": "2 puffs", "frequency": "as needed"},
        ],
        "recent_encounters": [
            {
                "date": "2025-08-20",
                "summary": "Asthma review, no recent exacerbations.",
            }
        ],
    },
}


DRUG_INFO: Dict[str, Dict[str, Any]] = {
    "atorvastatin": {
        "name": "atorvastatin",
        "class": "statin",
        "indications": [
            "hyperlipidemia",
            "cardiovascular risk reduction",
        ],
        "common_side_effects": [
            "myalgia",
            "gastrointestinal upset",
        ],
        "warnings": [
            "monitor liver function",
            "report unexplained muscle pain or weakness",
        ],
    },
    "lisinopril": {
        "name": "lisinopril",
        "class": "ACE inhibitor",
        "indications": [
            "hypertension",
            "heart failure",
        ],
        "common_side_effects": [
            "cough",
            "dizziness",
        ],
        "warnings": [
            "avoid in pregnancy",
            "monitor renal function and potassium",
        ],
    },
    "metformin": {
        "name": "metformin",
        "class": "biguanide",
        "indications": [
            "type 2 diabetes mellitus",
        ],
        "common_side_effects": [
            "gastrointestinal upset",
        ],
        "warnings": [
            "use caution in renal impairment",
            "rare risk of lactic acidosis",
        ],
    },
}


GUIDELINES: Dict[str, Dict[str, Any]] = {
    "fever_child": {
        "topic": "fever_child",
        "title": "Fever in children - basic guidance",
        "summary": (
            "For most otherwise healthy children with fever, focus on hydration, "
            "comfort, and monitoring. Seek urgent or emergency care if the child "
            "has difficulty breathing, persistent vomiting, poor responsiveness, "
            "a stiff neck, a rash that does not blanch, or any concerning symptoms."
        ),
    },
    "tension_headache": {
        "topic": "tension_headache",
        "title": "Tension type headache - basic guidance",
        "summary": (
            "For mild headaches associated with muscle tension or prolonged screen time, "
            "consider rest, hydration, ergonomics, and breaks. Seek urgent care for "
            "sudden severe headaches, neurologic changes, or other red flag features."
        ),
    },
}


def get_patient(patient_id: str) -> PatientRecord | None:
    return PATIENTS.get(patient_id)


def list_patients() -> List[str]:
    return list(PATIENTS.keys())


def get_drug(name: str) -> Dict[str, Any] | None:
    return DRUG_INFO.get(name.lower())


def get_guideline(topic: str) -> Dict[str, Any] | None:
    return GUIDELINES.get(topic)
