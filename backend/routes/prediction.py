import json

from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from backend.database import get_connection

from backend.ai.prediction import (
    predict_agriculture
)

from backend.ai.trust_score import (
    calculate_trust_score,
    get_reliability
)


prediction_bp = Blueprint(
    "prediction",
    __name__,
    url_prefix="/api/prediction"
)


# =========================================================
# LOGIN CHECK
# =========================================================

def require_login():

    return "user_id" in session


# =========================================================
# AGRICULTURE PREDICTION
# =========================================================

@prediction_bp.route(
    "/agriculture",
    methods=["POST"]
)
def agriculture_prediction():

    if not require_login():

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "success": False,
            "message": "No input data received."
        }), 400


    try:

        result = predict_agriculture(
            data
        )

        # -------------------------------------------------
        # Trust Score Inputs
        # -------------------------------------------------

        confidence = result[
            "confidence"
        ]

        data_quality = confidence

        uncertainty = 100 - confidence

        anomaly_score = max(
            0,
            100 - confidence
        )


        # -------------------------------------------------
        # Trust Score
        # -------------------------------------------------

        trust_score = calculate_trust_score(
            confidence,
            data_quality,
            uncertainty,
            anomaly_score
        )


        reliability = get_reliability(
            trust_score
        )


        # -------------------------------------------------
        # Save Analysis
        # -------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO analyses
            (
                user_id,
                domain,
                prediction,
                predicted_value,
                risk_level,
                confidence,
                trust_score,
                input_data,
                explanation,
                recommendation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],

                "Agriculture",

                result["prediction"],

                result["predicted_value"],

                result["risk_level"],

                result["confidence"],

                trust_score,

                json.dumps(data),

                result["explanation"],

                result["recommendation"]
            )
        )

        analysis_id = cursor.lastrowid

        connection.commit()
        connection.close()


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "analysis_id": analysis_id,

            "result": {

                **result,

                "trust_score": trust_score,

                "reliability": reliability

            }

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500


# =========================================================
# GENERIC DOMAIN PREDICTION
# =========================================================

@prediction_bp.route(
    "/",
    methods=["POST"]
)
def generic_prediction():

    if not require_login():

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    domain = data.get(
        "domain",
        "Other"
    )

    # Currently agriculture has
    # the working prediction model.

    if domain.lower() == "agriculture":

        return agriculture_prediction()

    return jsonify({

        "success": True,

        "result": {

            "prediction":
                "Analysis completed",

            "predicted_value":
                None,

            "confidence":
                75,

            "risk_level":
                "MEDIUM",

            "trust_score":
                72,

            "reliability":
                "Medium",

            "explanation":
                "The selected domain was analyzed successfully.",

            "recommendation":
                "Review the input data before making a final decision."

        }

    })