import json
import os

def read_json(path):
    """
    Safely read a JSON file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    """
    Safely write a JSON file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
