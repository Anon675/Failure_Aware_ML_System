def accuracy(predictions, labels):
    """
    Compute accuracy score.
    """
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must be same length")

    correct = 0
    for p, l in zip(predictions, labels):
        if p == l:
            correct += 1

    return correct / len(predictions)


def confidence_stats(confidences):
    """
    Compute basic confidence statistics.
    """
    if not confidences:
        return {
            "min": 0.0,
            "max": 0.0,
            "avg": 0.0
        }

    return {
        "min": min(confidences),
        "max": max(confidences),
        "avg": sum(confidences) / len(confidences)
    }
