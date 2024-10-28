from pydantic import BaseModel
from typing import Optional, List


class DiagnosisSchema(BaseModel):
    conclusion: str
    note: Optional[str] = None
    date: Optional[str] = None


class MedicationSchema(BaseModel):
    medication: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    instruction: Optional[str] = None
    date: Optional[str] = None
    summary: Optional[str] = None


class PatientSchema(BaseModel):
    gender: Optional[str] = None
    dob: Optional[str] = None
    blood_group: Optional[str] = None
    ethnicity: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None


class VitalSignSchema(BaseModel):
    pulse: Optional[float] = None
    body_temp: Optional[float] = None
    blood_pressure_high: Optional[float] = None
    blood_pressure_low: Optional[float] = None
    respiration_rate: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    neck: Optional[float] = None
    hip: Optional[float] = None
    bmi: Optional[float] = None
    body_fat: Optional[float] = None
    waist: Optional[float] = None
    ffmi: Optional[float] = None
    date: Optional[str] = None
# need to learn more about SPO2 information    


class LabResultSchema(BaseModel):
    lab_group_code: Optional[str] = None
    lab_code: Optional[str] = None
    value_string: Optional[str] = None
    value_quantity: Optional[float] = None
    unit: Optional[str] = None
    range: Optional[str] = None
    interpretation: Optional[str] = None
    note: Optional[str] = None
    date: Optional[str] = None
    summary: Optional[str] = None


class LabCodeSchema(BaseModel):
    code: str


class EncounterSchema(BaseModel):
    id: str
    patient_id: str
    performed_date: str
    re_examination_date: Optional[str] = None
    patient_info: Optional[PatientSchema] = None
    medications: Optional[List[MedicationSchema]] = []
    diagnosis: Optional[List[DiagnosisSchema]] = []
    vital_signs: Optional[List[VitalSignSchema]] = []
    lab_results: Optional[List[LabResultSchema]] = []
