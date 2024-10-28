from pydantic import BaseModel
from typing import Optional


class DiagnosisSchema(BaseModel):
    encounter_id: str
    patient_id: str
    conclusion: str
    note: Optional[str] = None
