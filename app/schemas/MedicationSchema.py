from pydantic import BaseModel
from typing import Optional


class MedicationSchema(BaseModel):
    id: str
    encounter_id: str
    patient_id: str
    medication: str
    quantity: int
    unit: str
    instruction: str
