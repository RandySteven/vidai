import json

def encode_json_str(data) -> str:
    json_string = json.dumps(data)
    return json_string

def decode_json_str(json_str: str):
    data = json.loads(json_str)
    return data