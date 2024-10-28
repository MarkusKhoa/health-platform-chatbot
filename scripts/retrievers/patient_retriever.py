import sqlite3
from typing import Optional
from scripts.schemas.common_schema import PatientSchema
from scripts.retrievers import DB


def fetch_patient(patient_id: str, jwt_token: str = None) -> Optional[PatientSchema]:
    patient = None
    return PatientSchema.model_validate(patient) if patient else None
