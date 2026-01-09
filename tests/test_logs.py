import json
import os

LOG_FILE = "logs/system_log.jsonl"


def test_logs():
    assert os.path.exists(LOG_FILE), "Log file does not exist"

    with open(LOG_FILE, "r") as f:
        line = f.readline()
        record = json.loads(line)

    required_fields = [
        "domain",
        "confidence",
        "failures",
        "decision",
        "timestamp"
    ]

    for field in required_fields:
        assert field in record, f"Missing log field: {field}"

    print("[PASS] Log integrity test")


if __name__ == "__main__":
    test_logs()
