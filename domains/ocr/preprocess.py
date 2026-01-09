from PIL import Image

def preprocess(image_path):
    """
    Loads image and converts to RGB.
    """
    image = Image.open(image_path).convert("RGB")
    return image_path
