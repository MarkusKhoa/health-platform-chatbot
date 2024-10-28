import sqlite3
from langchain_core.runnables import ensure_config
from langchain_core.tools import tool
from typing import Optional, List
from datetime import date
from scripts.retrievers.encounter_retriever import format_encounters_query_results
from scripts.schemas.args_schema import FetchRecentEncountersInputSchema
from scripts.tools import DB


@tool(args_schema=FetchRecentEncountersInputSchema)
def fetch_recent_encounters(
    limit: int = 5,
    additional_fields: List[str] = []
) -> list[dict]:
    """Fetch recent encounters sorted by date for the patient along with corresponding patient information and diagnosis information.

    Args:
        limit (int): The number of encounters returned
        additional_fields (List[str]): The fields needed to answer the question. Possibles values must be: diagnosis, medications, lab_results, vital_signs

    Returns:
        A list of dictionaries where each dictionary contains the encounters details,
        associated patient information, encounter's diagnosis information belonging to the patient.
    """
    print(additional_fields)
    config = ensure_config()  # Fetch from the context
    configuration = config.get("configurable", {})
    patient_id = configuration.get("patient_id", None)
    if not patient_id:
        raise ValueError("No patient ID configured.")
    encounters = []
    return encounters


@tool
def search_encounters(
    performed_date: Optional[date] = None,
    limit: int = 5
) -> list[dict]:
    """Search for encounters based on performed date.

    Args:
        performed_date (Optional[date]): The date that perform the encounter

    Returns:
        A list of dictionaries where each dictionary contains the encounters details,
        associated patient information, encounter's diagnosis information belonging to the user.
    """
    config = ensure_config()  # Fetch from the context
    configuration = config.get("configurable", {})
    patient_id = configuration.get("patient_id", None)
    if not patient_id:
        raise ValueError("No patient ID configured.")
    encounters = []
    return encounters
