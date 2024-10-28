import sqlite3
from typing import Optional, List
from scripts.schemas.common_schema import DiagnosisSchema
from scripts.retrievers import DB


def fetch_diagnosis(encounter_id: str, jwt_token: str = None) -> List[DiagnosisSchema]:
    results = []
    return results
