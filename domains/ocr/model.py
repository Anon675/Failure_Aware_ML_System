import pytesseract
from PIL import Image

class OCRModel:
    """
    OCR model using Tesseract.
    """

    def predict(self, image_path):
        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        confidence = min(len(text) / 100, 1.0)

        return text, confidence
