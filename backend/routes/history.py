from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from backend.database import get_connection


history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/api/history"
)


# =========================================================
# GET HISTORY
# =========================================================

@history_bp.route(
    "",
    methods=["GET"]
)
def get_history():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            id,
            domain,
            prediction,
            predicted_value,
            risk_level,
            confidence,
            trust_score,
            explanation,
            recommendation,
            created_at
        FROM analyses
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (
            session["user_id"],
        )
    )


    rows = cursor.fetchall()

    connection.close()


    analyses = [
        dict(row)
        for row in rows
    ]


    return jsonify({

        "success": True,

        "count": len(analyses),

        "analyses": analyses

    })


# =========================================================
# SINGLE HISTORY ITEM
# =========================================================

@history_bp.route(
    "/<int:analysis_id>",
    methods=["GET"]
)
def get_analysis(analysis_id):

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM analyses
        WHERE id = ?
        AND user_id = ?
        """,
        (
            analysis_id,
            session["user_id"]
        )
    )


    row = cursor.fetchone()

    connection.close()


    if not row:

        return jsonify({
            "success": False,
            "message": "Analysis not found."
        }), 404


    return jsonify({

        "success": True,

        "analysis": dict(row)

    })


# =========================================================
# DELETE HISTORY ITEM
# =========================================================

@history_bp.route(
    "/<int:analysis_id>",
    methods=["DELETE"]
)
def delete_analysis(analysis_id):

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401


    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM analyses
        WHERE id = ?
        AND user_id = ?
        """,
        (
            analysis_id,
            session["user_id"]
        )
    )


    connection.commit()

    deleted = cursor.rowcount

    connection.close()


    if deleted == 0:

        return jsonify({
            "success": False,
            "message": "Analysis not found."
        }), 404


    return jsonify({

        "success": True,

        "message":
            "Analysis deleted successfully."

    })