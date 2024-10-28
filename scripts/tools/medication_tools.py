import sqlite3
from langchain_core.runnables import ensure_config
from langchain_core.tools import tool
from typing import Optional, List
from datetime import date
from scripts.schemas.common_schema import MedicationSchema
from scripts.schemas.args_schema import MedicationsSearchArgsSchema
from scripts.helpers.format_text import convert_to_sql_fields
from scripts.tools import DB


@tool(args_schema=MedicationsSearchArgsSchema)
def search_medicines(
    performed_date: Optional[date] = None,
    needed_fields: List[str] = [],
    limit: int = 10
) -> list[dict]:
    """Useful to search and retrieve patient medicines based on performed date

    Args:
        performed_date (Optional[date]): The date that perform examination

    Returns:
        A list of dictionaries where each dictionary contains the medicine detail (medication name, quantity, unit and usage instruction)
    """
    config = ensure_config()  # Fetch from the context
    configuration = config.get("configurable", {})
    patient_id = configuration.get("patient_id", None)
    if not patient_id:
        raise ValueError("No patient ID configured.")
    results = []
    return results
