class InferenceEngine:
    """
    This class runs the ML model.
    It does NOT judge correctness.
    """

    def run(self, model, input_data):
        """
        model: domain-specific model object
        input_data: preprocessed input
        """

        try:
            prediction, confidence = model.predict(input_data)

            return {
                "prediction": prediction,
                "confidence": confidence,
                "error": None
            }

        except Exception as e:
            return {
                "prediction": None,
                "confidence": 0.0,
                "error": str(e)
            }
