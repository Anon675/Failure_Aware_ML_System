import statistics

class UncertaintyEngine:
    """
    Estimates uncertainty using multiple inference runs.
    """

    def evaluate(self, confidence_scores):
        mean_conf = statistics.mean(confidence_scores)
        variance = statistics.pvariance(confidence_scores)

        return {
            "mean_confidence": mean_conf,
            "variance": variance,
            "is_unstable": variance > 0.02
        }
