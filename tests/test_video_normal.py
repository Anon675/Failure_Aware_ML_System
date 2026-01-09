import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domains.video.signals import extract_signals
from core.failure_detector import FailureDetector
from core.router import Router


def test_normal_video():
    # Simulate normal-length video
    frames = ["f1", "f2", "f3", "f4", "f5"]

    signals = extract_signals(frames)

    detector = FailureDetector()
    failures = detector.detect(
        inference_result={"error": None},
        confidence_result={"is_low": False},
        domain_signals=signals
    )

    router = Router()
    decision = router.route(failures)

    assert decision == "auto_accept", "Normal video should be auto accepted"

    print("[PASS] Normal video auto accepted")


if __name__ == "__main__":
    test_normal_video()
