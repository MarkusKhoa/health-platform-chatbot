import sqlite3
from typing import Optional, List
from scripts.schemas.common_schema import LabCodeSchema
from scripts.retrievers import DB
import httpx
from app.config.AppSettings import get_app_settings

app_settings = get_app_settings()


def search_lab_codes(lab_name:  str) -> List[str]:
    url = f"{app_settings.terminology_endpoint}/labs/search?lab_name={lab_name}&limit=10&fields=id,code"
    try:
        response = httpx.get(url=url, headers={
            "x-api-key": app_settings.terminology_api_key
        })
        response.raise_for_status()
        data = response.json()
        lab_codes = [lab["code"] for lab in data["data"] if "code" in lab]
        # print(lab_name)
        # print(lab_codes)
        return lab_codes
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
    return []

    # conn = sqlite3.connect(DB)
    # cursor = conn.cursor()
    # query = "SELECT code FROM lab_codes WHERE searchable_words LIKE '%' || ? || '%';"
    # cursor.execute(query, (lab_name,))
    # rows = cursor.fetchall()
    # column_names = [column[0] for column in cursor.description]
    # results = [LabCodeSchema.model_validate(
    #     dict(zip(column_names, row))) for row in rows]
    # return results
