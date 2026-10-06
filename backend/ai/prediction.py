def predict_agriculture(data):

    temperature = float(
        data.get("temperature", 25)
    )

    humidity = float(
        data.get("humidity", 70)
    )

    rainfall = float(
        data.get("rainfall", 800)
    )

    soil_ph = float(
        data.get("soil_ph", 6.5)
    )

    nitrogen = float(
        data.get("nitrogen", 80)
    )

    phosphorus = float(
        data.get("phosphorus", 40)
    )

    potassium = float(
        data.get("potassium", 45)
    )


    # -----------------------------------------------------
    # BASIC AGRICULTURE MODEL
    # -----------------------------------------------------

    score = 50


    # Temperature
    if 20 <= temperature <= 32:
        score += 8
    else:
        score -= 8


    # Humidity
    if 50 <= humidity <= 85:
        score += 7
    else:
        score -= 5


    # Rainfall
    if 500 <= rainfall <= 1200:
        score += 8
    else:
        score -= 8


    # Soil pH
    if 5.5 <= soil_ph <= 7.5:
        score += 8
    else:
        score -= 8


    # Nitrogen
    if 40 <= nitrogen <= 120:
        score += 5
    else:
        score -= 5


    # Phosphorus
    if 20 <= phosphorus <= 80:
        score += 4
    else:
        score -= 4


    # Potassium
    if 20 <= potassium <= 100:
        score += 4
    else:
        score -= 4


    score = max(
        0,
        min(100, score)
    )


    # -----------------------------------------------------
    # YIELD
    # -----------------------------------------------------

    predicted_yield = round(
        3.0 + (score / 100) * 3.0,
        1
    )


    # -----------------------------------------------------
    # CONFIDENCE
    # -----------------------------------------------------

    confidence = round(
        60 + score * 0.35
    )

    confidence = min(
        98,
        max(50, confidence)
    )


    # -----------------------------------------------------
    # RISK
    # -----------------------------------------------------

    if score >= 75:

        risk_level = "LOW"

    elif score >= 55:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    explanation = (
        "The prediction was generated using "
        "temperature, humidity, rainfall, soil pH "
        "and nutrient conditions."
    )


    # -----------------------------------------------------
    # RECOMMENDATION
    # -----------------------------------------------------

    if risk_level == "LOW":

        recommendation = (
            "Input conditions are suitable. "
            "The prediction has good reliability."
        )

    elif risk_level == "MEDIUM":

        recommendation = (
            "Review soil and weather conditions "
            "before making a final decision."
        )

    else:

        recommendation = (
            "The input conditions show significant "
            "uncertainty. Collect additional data."
        )


    return {

        "prediction": "Crop Yield Prediction",

        "predicted_value": predicted_yield,

        "unit": "tonnes/hectare",

        "confidence": confidence,

        "risk_level": risk_level,

        "explanation": explanation,

        "recommendation": recommendation
    }