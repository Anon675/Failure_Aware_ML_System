import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.router import Router


def test_routing():
    router = Router()

    # Case 1: failures exist → human review
    failures = ["low_confidence"]
    decision = router.route(failures)
    assert decision == "human_review", "Routing failed for risky input"

    # Case 2: no failures → auto accept
    failures = []
    decision = router.route(failures)
    assert decision == "auto_accept", "Routing failed for safe input"

    print("[PASS] Routing correctness test")


if __name__ == "__main__":
    test_routing()
