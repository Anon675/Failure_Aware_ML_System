import os

def validate_file_exists(path):
    """
    Check if input file exists.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    return True


def validate_not_empty(value, name="value"):
    """
    Check if a value is not empty.
    """
    if value is None or value == "":
        raise ValueError(f"{name} cannot be empty")
    return True
