from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict
from datetime import date


class SearchAgentQuestionSchema(BaseModel):
    question: str


class SearchAgentAnswerSchema(BaseModel):
    answer: str
