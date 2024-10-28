from pydantic import BaseModel
from typing import Optional


class PatientSchema(BaseModel):
    id: str
    gender: str
    dob: str
    blood_group: str
    ethnicity: str
    nationality: str
    address: str
    occupation: str
