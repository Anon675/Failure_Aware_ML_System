import argparse

# Core
from core.inference_engine import InferenceEngine
from core.uncertainty_engine import UncertaintyEngine
from core.stability_engine import StabilityEngine
from core.fusion_engine import FusionEngine
from core.failure_detector import FailureDetector
from core.failure_reasoner import FailureReasoner
from core.router import Router
from core.logger import SystemLogger

# OCR
from domains.ocr.model import OCRModel
from domains.ocr.preprocess import preprocess as ocr_preprocess
from domains.ocr.postprocess import postprocess as ocr_postprocess
from domains.ocr.signals import extract_signals as ocr_signals

# Medical
from domains.medical.model import MedicalModel
from domains.medical.preprocess import preprocess as medical_preprocess
from domains.medical.postprocess import postprocess as medical_postprocess
from domains.medical.signals import extract_signals as medical_signals

# Video
from domains.video.model import VideoModel
from domains.video.preprocess import preprocess as video_preprocess
from domains.video.postprocess import postprocess as video_postprocess
from domains.video.signals import extract_signals as video_signals


def main():
    parser = argparse.ArgumentParser("Failure-Aware ML System v2.0")
    parser.add_argument("--domain", required=True, choices=["ocr", "medical", "video"])
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    # Engines
    inference_engine = InferenceEngine()
    uncertainty_engine = UncertaintyEngine()
    stability_engine = StabilityEngine()
    fusion_engine = FusionEngine()
    failure_detector = FailureDetector()
    failure_reasoner = FailureReasoner()
    router = Router()
    logger = SystemLogger()

    predictions = []
    confidences = []

    # -------- DOMAIN SWITCH -------- #

    if args.domain == "ocr":
        model = OCRModel()
        processed = ocr_preprocess(args.input)

        for _ in range(3):
            result = inference_engine.run(model, processed)
            predictions.append(result["prediction"])
            confidences.append(result["confidence"])

        signals = ocr_signals(predictions[0])
        final_output = ocr_postprocess(predictions[0])

    elif args.domain == "medical":
        model = MedicalModel()
        processed = medical_preprocess(args.input)

        for _ in range(3):
            result = inference_engine.run(model, processed)
            predictions.append(result["prediction"])
            confidences.append(result["confidence"])

        signals = medical_signals(image_quality=0.7)
        final_output = medical_postprocess(predictions[0])

    elif args.domain == "video":
        model = VideoModel()
        frames = video_preprocess(args.input)

        for _ in range(3):
            result = inference_engine.run(model, frames)
            predictions.append(result["prediction"])
            confidences.append(result["confidence"])

        signals = video_signals(frames)
        final_output = video_postprocess(predictions[0])

    # -------- v2.0 LOGIC -------- #

    uncertainty = uncertainty_engine.evaluate(confidences)
    stable = stability_engine.is_stable(predictions)

    fusion_failures = fusion_engine.fuse(uncertainty, stable)

    base_failures = failure_detector.detect(
        inference_result={"error": None},
        confidence_result={"is_low": uncertainty["mean_confidence"] < 0.6},
        domain_signals=signals
    )

    failures = base_failures + fusion_failures
    explanations = failure_reasoner.explain(failures)

    log_record = {
        "domain": args.domain,
        "input": args.input,
        "predictions": predictions,
        "mean_confidence": uncertainty["mean_confidence"],
        "confidence_variance": uncertainty["variance"],
        "failures": failures,
        "explanations": explanations
    }

    decision = router.route(failures, log_record)
    log_record["decision"] = decision
    log_record["final_output"] = final_output

    logger.log(log_record)

    print("\n--- RESULT (v2.0) ---")
    print("Domain:", args.domain)
    print("Decision:", decision)
    print("Mean Confidence:", uncertainty["mean_confidence"])
    print("Variance:", uncertainty["variance"])
    print("Failures:", failures)


if __name__ == "__main__":
    main()
