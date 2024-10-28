import sqlite3
from typing import Optional, List
from scripts.schemas.common_schema import LabResultSchema
from scripts.retrievers import DB


def fetch_lab_results(encounter_id: str, jwt_token: str = None) -> List[LabResultSchema]:
    results = []
    return results
