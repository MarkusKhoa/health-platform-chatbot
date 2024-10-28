from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict
from datetime import date


class HealthAgentQuestionSchema(BaseModel):
    patient_id: str
    message: str


class HealthAgentAnswerSchema(BaseModel):
    content: str
