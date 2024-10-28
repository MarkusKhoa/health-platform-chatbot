import sqlite3
from typing import Optional, List
from scripts.schemas.common_schema import VitalSignSchema
from scripts.retrievers import DB


def fetch_vital_signs(encounter_id: str, jwt_token: str = None) -> List[VitalSignSchema]:
    results = []
    return results
