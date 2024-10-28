import sqlite3
from typing import Optional, List
from scripts.schemas.common_schema import MedicationSchema
from scripts.retrievers import DB


def fetch_medications(encounter_id:  str, jwt_token: str = None) -> List[MedicationSchema]:
    results = []
    return results
