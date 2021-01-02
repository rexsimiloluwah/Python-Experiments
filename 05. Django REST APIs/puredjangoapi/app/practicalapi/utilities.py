import json

def validate_json(data):
    is_valid = False
    try:
        json_data = json.loads(data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
