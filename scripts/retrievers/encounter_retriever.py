import sqlite3
import json
from typing import Optional, List
from datetime import date
from scripts.schemas.common_schema import EncounterSchema
from scripts.retrievers.diagnosis_retriever import fetch_diagnosis
from scripts.retrievers.patient_retriever import fetch_patient
from scripts.retrievers.medication_retriever import fetch_medications
from scripts.retrievers.vital_sign_retriever import fetch_vital_signs
from scripts.retrievers.lab_result_retriever import fetch_lab_results
from scripts.retrievers import DB, patient_id


def format_encounters_query_results(query_results: list[dict], patient_id: str, additional_fields: list[str] = [], jwt_token: str = None) -> list[dict]:
    encounters = []
    for e in query_results:
        encounter = EncounterSchema.model_validate(e)
        encounter_id = encounter.id
        patient_info = fetch_patient(patient_id, jwt_token)
        encounter.patient_info = patient_info
        if "diagnosis" in additional_fields:
            diagnoses = fetch_diagnosis(encounter_id, jwt_token)
            encounter.diagnosis = diagnoses
        if "medications" in additional_fields:
            medications = fetch_medications(encounter_id, jwt_token)
            encounter.medications = medications
        if "vital_signs" in additional_fields:
            vital_signs = fetch_vital_signs(encounter_id, jwt_token)
            encounter.vital_signs = vital_signs
        if "lab_results" in additional_fields:
            lab_results = fetch_lab_results(encounter_id, jwt_token)
            encounter.lab_results = lab_results
        encounters.append(encounter.model_dump(exclude_none=True))
    return encounters


def fetch_encounters() -> list[dict]:
    """Fetch 10 recent encounters for the user along with corresponding patient information and diganosis information.

    Returns:
        A list of dictionaries where each dictionary contains the encounters details,
        associated patient information, encounter's diagnosis information belonging to the user.
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = """
    SELECT
        e.id AS encounter_d,
        e.performed_date,
        e.diagnosis_note,
        p.id AS patient_id,
        p.gender AS patient_gender,
        p.dob AS patient_dob,
        p.blood_group,
        p.ethnicity,
        p.nationality,
        p.address,
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


def search_encounters(
    performed_date: Optional[date] = None,
    limit: int = 5
) -> list[dict]:
    """Search for encounters based on performed date.

    Returns:
        A list of dictionaries where each dictionary contains the encounters details,
        associated patient information, encounter's diagnosis information belonging to the user.
    """

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = """
    SELECT
        *
    FROM
        encounters e
    WHERE
    """
    query += "\n\te.patient_id = ?"
    params = []
    params.append(patient_id)

    if performed_date:
        query += "\n\tAND e.performed_date = ?"
        params.append(str(performed_date))

    query += "\nORDER BY\n\te.performed_date DESC;"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    query_results = [dict(zip(column_names, row)) for row in rows]
    encounters = format_encounters_query_results(query_results)
    cursor.close()
    conn.close()

    return encounters
