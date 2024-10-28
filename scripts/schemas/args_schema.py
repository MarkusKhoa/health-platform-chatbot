from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class FetchRecentEncountersInputSchema(BaseModel):
    limit: int = Field(
        description="The number of encounters returned", default=5)
    additional_fields: List[str] = Field(
        description="The fields needed to answer the question. Possibles values must be: diagnosis, medications, lab_results, vital_signs", default=[])


class LabResultsSearchArgsSchema(BaseModel):
    lab_name: Optional[str] = Field(
        description="The lab name in Vietnamese", default=None)
    performed_date: Optional[date] = None
    needed_fields: List[str] = Field(
        description="The lab result fields needed to answer the question. Possibles values must be: lab_group_code, lab_code, value_string, value_quantity, unit, range, interpretation")
    limit: int = Field(
        description="The number of encounters returned", default=10)


class MedicationsSearchArgsSchema(BaseModel):
    lab_name: Optional[str] = None,
    needed_fields: List[str] = Field(
        description="The medication fields needed to answer the question. Possibles values must be: medication, quantity, unit, instruction")
    limit: int = Field(
        description="The number of encounters returned", default=5)


class VitalSignsSearchArgsSchema(BaseModel):
    lab_name: Optional[str] = None,
    needed_fields: List[str] = Field(
        description="The vital sign fields needed to answer the question. Possibles values must be: pulse, body_temp, blood_pressure_high, blood_pressure_low, respiration_rate, weight, height, neck, hip, bmi, body_fat, waist, ffmi")
    limit: int = Field(
        description="The number of encounters returned", default=5)
