import random

class MedicalModel:
    """
    Simulated fracture detection model.
    """

    def predict(self, image_tensor):
        prediction = random.choice(["fracture", "no_fracture"])
        confidence = random.uniform(0.6, 0.95)

        return prediction, confidence
