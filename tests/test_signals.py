import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domains.ocr.signals import extract_signals as ocr_signals
from domains.video.signals import extract_signals as video_signals
from domains.medical.signals import extract_signals as medical_signals


def test_signals():
    # OCR: non-ascii text should fail
    bad_text = "— — —"
    ocr_result = ocr_signals(bad_text)
    assert ocr_result["contains_non_ascii"] is False

    # Video: too few frames should fail
    frames = ["frame1"]
    video_result = video_signals(frames)
    assert video_result["enough_frames"] is False

    # Medical: low image quality should fail
    medical_result = medical_signals(image_quality=0.3)
    assert medical_result["image_quality_ok"] is False

    print("[PASS] Failure signal coverage test")


if __name__ == "__main__":
    test_signals()
