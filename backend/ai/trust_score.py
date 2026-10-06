def calculate_trust_score(
    confidence,
    data_quality,
    uncertainty,
    anomaly_score
):

    score = 0

    # Confidence
    score += confidence * 0.40

    # Data quality
    score += data_quality * 0.30

    # Lower uncertainty = better
    score += (100 - uncertainty) * 0.15

    # Lower anomaly = better
    score += (100 - anomaly_score) * 0.15

    score = round(score)

    score = max(
        0,
        min(100, score)
    )

    return score


def get_reliability(score):

    if score >= 80:
        return "High"

    if score >= 60:
        return "Medium"

    return "Low"