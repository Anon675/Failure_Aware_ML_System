import json
import os
from datetime import datetime

class Router:
    """
    Decides what action to take.
    """

    def route(self, failures, record=None):
        if len(failures) > 0:
            if record is not None:
                self.send_to_human_review(record)
            return "human_review"
        return "auto_accept"

    def send_to_human_review(self, record):
        os.makedirs("human_review/queue", exist_ok=True)

        record["timestamp"] = datetime.utcnow().isoformat()
        record["human_verdict"] = {
            "status": "pending",
            "comments": ""
        }

        filename = f"review_{int(datetime.utcnow().timestamp())}.json"
        path = os.path.join("human_review/queue", filename)

        with open(path, "w") as f:
            json.dump(record, f, indent=2)
