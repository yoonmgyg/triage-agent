from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from healthcare_data import get_patient, get_drug, get_guideline, list_patients


app = FastAPI(title="Healthcare MCP style server")


class EHRRequest(BaseModel):
    patient_id: str


class DrugRequest(BaseModel):
    drug_name: str


class GuidelineRequest(BaseModel):
    topic: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/tools/patients")
def patients_list() -> Dict[str, Any]:
    return {"patients": list_patients()}


@app.post("/tools/ehr_lookup")
def ehr_lookup(req: EHRRequest) -> Dict[str, Any]:
    record = get_patient(req.patient_id)
    if record is None:
        raise HTTPException(status_code=404, detail="patient_not_found")
    return {"record": record}


@app.post("/tools/drug_info")
def drug_info(req: DrugRequest) -> Dict[str, Any]:
    info = get_drug(req.drug_name)
    if info is None:
        raise HTTPException(status_code=404, detail="drug_not_found")
    return {"drug": info}


@app.post("/tools/guideline_lookup")
def guideline_lookup(req: GuidelineRequest) -> Dict[str, Any]:
    info = get_guideline(req.topic)
    if info is None:
        raise HTTPException(status_code=404, detail="guideline_not_found")
    return {"guideline": info}
