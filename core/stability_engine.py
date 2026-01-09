class StabilityEngine:
    """
    Checks if predictions are consistent across runs.
    """

    def is_stable(self, predictions):
        return len(set(predictions)) == 1
