import json
def clean_json(json_text:str) -> list:
    cleaned_json = json_text.strip()
    cleaned_json = cleaned_json.removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
