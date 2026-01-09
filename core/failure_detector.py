class FailureDetector:
    """
    Detects failure signals from outputs.
    """

    def detect(self, inference_result, confidence_result, domain_signals):
        failures = []

        if inference_result["error"] is not None:
            failures.append("model_error")

        if confidence_result["is_low"]:
            failures.append("low_confidence")

        for signal, value in domain_signals.items():
            if value is False:
                failures.append(f"signal_failed:{signal}")

        return failures
