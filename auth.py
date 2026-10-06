from flask import Blueprint, request, jsonify, session

from backend.database import get_connection
from backend.utils.security import (
    hash_password,
    verify_password
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# =========================================================
# SIGNUP
# =========================================================

@auth_bp.route(
    "/signup",
    methods=["POST"]
)
def signup():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    name = str(
        data.get("name", "")
    ).strip()

    email = str(
        data.get("email", "")
    ).strip().lower()

    password = str(
        data.get("password", "")
    )

    if not name or not email or not password:

        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    if len(password) < 6:

        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    existing = cursor.fetchone()

    if existing:

        connection.close()

        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            password
        )
        VALUES (?, ?, ?)
        """,
        (
            name,
            email,
            hash_password(password)
        )
    )

    user_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO settings
        (
            user_id
        )
        VALUES (?)
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()

    session["user_id"] = user_id
    session["user_name"] = name
    session["user_email"] = email

    return jsonify({
        "success": True,
        "message": "Account created successfully.",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }), 201


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    email = str(
        data.get("email", "")
    ).strip().lower()

    password = str(
        data.get("password", "")
    )

    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if not user:

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    if not verify_password(
        password,
        user["password"]
    ):

        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "message": "Welcome back!",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    })


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    })


# =========================================================
# CURRENT USER
# =========================================================

@auth_bp.route(
    "/me",
    methods=["GET"]
)
def current_user():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Not logged in."
        }), 401

    return jsonify({
        "success": True,
        "user": {
            "id": session["user_id"],
            "name": session["user_name"],
            "email": session["user_email"]
        }
    })