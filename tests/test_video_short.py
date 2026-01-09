import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domains.video.signals import extract_signals
from core.failure_detector import FailureDetector
from core.router import Router


def test_short_video():
    # Simulate very short video (too few frames)
    frames = ["frame1"]

    # Extract video-specific signals
    signals = extract_signals(frames)

    detector = FailureDetector()
    failures = detector.detect(
        inference_result={"error": None},
        confidence_result={"is_low": False},
        domain_signals=signals
    )

    router = Router()
    decision = router.route(failures)

    assert decision == "human_review", "Short video should be routed to human review"

    print("[PASS] Short video routed to human review")


if __name__ == "__main__":
    test_short_video()
