import sys
import os
import json

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

QUEUE_DIR = "human_review/queue"


def test_human_review():
    assert os.path.exists(QUEUE_DIR), "Human review queue does not exist"

    files = os.listdir(QUEUE_DIR)
    assert len(files) > 0, "No human review cases found"

    path = os.path.join(QUEUE_DIR, files[0])

    with open(path, "r") as f:
        record = json.load(f)

    # Status can be pending or already reviewed
    assert record["human_verdict"]["status"] in [
        "pending",
        "approved",
        "corrected",
        "rejected"
    ]

    # Simulate human review update
    record["human_verdict"]["status"] = "approved"
    record["human_verdict"]["comments"] = "Reviewed and approved by test script"

    with open(path, "w") as f:
        json.dump(record, f, indent=2)

    print("[PASS] Human review lifecycle test")


if __name__ == "__main__":
    test_human_review()
