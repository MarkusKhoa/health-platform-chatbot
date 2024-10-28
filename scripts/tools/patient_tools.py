import sqlite3
from langchain_core.runnables import ensure_config
from langchain_core.tools import tool
from typing import Optional
from datetime import date
from scripts.schemas.common_schema import PatientSchema


db = "data/health.db"
patient_id = "1d9e7501-faed-4c8a-afc4-dae674ab4ae1"


@tool
def get_patient_information() -> list[dict]:
    """Call to get the patient information"""
    config = ensure_config()  # Fetch from the context
    configuration = config.get("configurable", {})
    patient_id = configuration.get("patient_id", None)
    if not patient_id:
        raise ValueError("No patient ID configured.")
    # Demo Patient
    patient = PatientSchema(
        gender="MALE",
        dob="1996-10-07",
        blood_group="A",
        nationality="VN",
        address="Ho Chi Minh City",
        occupation="Engineer"
    )
    return PatientSchema.model_validate(patient) if patient else None
