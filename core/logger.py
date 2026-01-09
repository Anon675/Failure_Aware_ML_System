import json
import os
from datetime import datetime

class SystemLogger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "system_log.jsonl")

    def log(self, record):
        record["timestamp"] = datetime.utcnow().isoformat()

        with open(self.log_file, "a") as f:
            f.write(json.dumps(record) + "\n")
