import json


def print_pretty(data: dict):
    json_formatted_str = json.dumps(data, indent=2, ensure_ascii=False)
    print(json_formatted_str)
