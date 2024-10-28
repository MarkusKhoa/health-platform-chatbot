import sqlite3
from datetime import date, datetime
from typing import Optional
from langchain_core.tools import tool
import pytz
from langchain_core.runnables import ensure_config
from app.utils.tool_utils import print_pretty
db = "data/health.db"


@tool
def fetch_user_encounter_information() -> list[dict]:
    """Fetch 10 recent encounters for the patient along with corresponding patient information and diagnosis information.

    Returns:
        A list of dictionaries where each dictionary contains the encounters details,
        associated patient information, encounter's diagnosis information belonging to the patient.
    """

    config = ensure_config()  # Fetch from the context
    configuration = config.get("configurable", {})
    patient_id = configuration.get("patient_id", None)
    if not patient_id:
        raise ValueError("No patient ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = """
    SELECT
        e.id AS encounter_d,
        e.performed_date,
        e.diagnosis_note,
        p.id AS patient_id,
        p.gender AS patient_gender,
        p.dob AS patient_dob,
        p.blood_group AS patient_blood_group,
        p.ethnicity AS patient_ethnicity,
        p.nationality AS patient_nationality,
        p.address AS patient_address,
        d.conclusion,
        d.note
    FROM
        encounters e
    JOIN
        patients p ON e.patient_id = p.id
    JOIN
        diagnoses d ON e.id = d.encounter_id
    WHERE
        e.patient_id = ?
    ORDER BY
        e.performed_date DESC;
    """
    cursor.execute(query, (patient_id,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()
    return results
