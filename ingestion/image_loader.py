from PIL import Image
import pytesseract


def load_image_text(path):
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text.strip()
