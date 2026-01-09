import random

class VideoModel:
    """
    Simplified video understanding model.
    """

    def predict(self, frames):
        prediction = "question_detected"
        confidence = random.uniform(0.5, 0.9)

        return prediction, confidence
