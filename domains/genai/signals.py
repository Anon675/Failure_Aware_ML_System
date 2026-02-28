def extract_signals(generated_text):
    signals = {
        "too_short": len(generated_text) > 20,
        "contains_uncertainty_words": not any(
            word in generated_text.lower()
            for word in ["maybe", "possibly", "i think", "not sure"]
        )
    }
    return signals
