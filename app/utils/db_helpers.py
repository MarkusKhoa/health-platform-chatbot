import sqlite3


def check_patient_id(patient_id):
    # Connect to the database
    conn = sqlite3.connect('data/health.db')
    cursor = conn.cursor()

    # Execute a SELECT query to check if the patient_id exists
    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE id = ?", (patient_id,))

    # Fetch the result
    result = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    # Return True if the patient_id exists, False otherwise
    return result > 0
