class FailureReasoner:
    """
    Translates failures into explanations.
    """

    def explain(self, failures):
        explanations = []

        for f in failures:
            if f == "low_confidence":
                explanations.append("Model confidence is below safe threshold.")
            elif f == "model_error":
                explanations.append("Model execution failed.")
            elif f.startswith("signal_failed"):
                explanations.append("One or more domain safety checks failed.")
            else:
                explanations.append("Unknown failure detected.")

        return explanations
