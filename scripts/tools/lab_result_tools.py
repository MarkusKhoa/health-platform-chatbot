import sqlite3
from langchain_core.runnables import ensure_config
from langchain_core.tools import tool
from typing import Optional, List
from datetime import date
from scripts.retrievers.lab_codes_retriever import search_lab_codes
from scripts.schemas.common_schema import LabResultSchema
from scripts.schemas.args_schema import LabResultsSearchArgsSchema
from scripts.helpers.format_text import convert_to_sql_fields
from scripts.tools import DB


@tool(args_schema=LabResultsSearchArgsSchema)
def search_lab_results(
    lab_name: Optional[str] = None,
    performed_date: Optional[date] = None,
    needed_fields: List[str] = [],
    limit: int = 10
) -> list[dict]:
    """Search lab results based on lab name and performed date

    Returns:
        A list of dictionaries where each dictionary contains the lab result details (value, unit, normal range and interpretation)
    """
    config = ensure_config()  # Fetch from the context
    configuration = config.get("configurable", {})
    patient_id = configuration.get("patient_id", None)
    if not patient_id:
        raise ValueError("No patient ID configured.")
    lab_codes = []
    if lab_name:
        lab_codes = search_lab_codes(lab_name)
    results = []
    return results
