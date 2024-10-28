def convert_to_sql_fields(fields: list[str], prefix: str):
    return ", ".join(f"{prefix}.{item}" for item in fields)
