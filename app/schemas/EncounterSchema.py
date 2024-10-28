from pydantic import BaseModel
from typing import Optional, List
from app.schemas.PatientSchema import PatientSchema
from app.schemas.DiagnosisSchema import DiagnosisSchema
from app.schemas.MedicationSchema import MedicationSchema


class EncounterSchema(BaseModel):
    id: str
    patient_id: str
    performed_date: str
    patient_info: Optional[PatientSchema]
    medications: List[MedicationSchema] = []
    diagnosis: Optional[DiagnosisSchema]
