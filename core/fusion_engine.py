class FusionEngine:
    """
    Combines uncertainty + stability into failure signals.
    """

    def fuse(self, uncertainty_result, prediction_stable):
        failures = []

        if uncertainty_result["is_unstable"]:
            failures.append("unstable_confidence")

        if not prediction_stable:
            failures.append("prediction_disagreement")

        return failures
