def extract_signals(text):
    signals = {
        "text_too_short": len(text) >= 5,
        "contains_non_ascii": text.isascii()
    }
    return signals
