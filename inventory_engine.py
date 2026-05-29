def readiness_score(stock, forecast):

    score = min(
        100,
        round(stock / (forecast + 1e-6) * 100)
    )

    if score >= 120:
        status = "Excellent"

    elif score >= 90:
        status = "Ready"

    elif score >= 70:
        status = "Moderate Risk"

    else:
        status = "High Risk"

    return score, status