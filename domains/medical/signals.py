def extract_signals(image_quality=0.7):
    return {
        "image_quality_ok": image_quality >= 0.5
    }
