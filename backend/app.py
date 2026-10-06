from flask import (
    Flask,
    jsonify
)

from flask_cors import CORS

from backend.config import (
    SECRET_KEY,
    HOST,
    PORT,
    DEBUG,
    FRONTEND_URL
)

from backend.database import (
    create_database
)

from backend.routes.auth import (
    auth_bp
)

from backend.routes.prediction import (
    prediction_bp
)

from backend.routes.history import (
    history_bp
)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__
)


# =========================================================
# CONFIG
# =========================================================

app.secret_key = SECRET_KEY


# =========================================================
# CORS
# =========================================================

CORS(
    app,

    supports_credentials=True,

    origins=[
        FRONTEND_URL,

        "http://localhost:5500",

        "http://127.0.0.1:5500"
    ]
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# BLUEPRINTS
# =========================================================

app.register_blueprint(
    auth_bp
)

app.register_blueprint(
    prediction_bp
)

app.register_blueprint(
    history_bp
)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({

        "success": True,

        "name": "TrustAI",

        "message":
            "TrustAI backend is running.",

        "version":
            "1.0.0"

    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    return jsonify({

        "success": True,

        "status": "online",

        "service": "TrustAI Backend"

    })


# =========================================================
# 404
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "success": False,

        "message":
            "API endpoint not found."

    }), 404


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       TRUSTAI BACKEND SERVER")
    print("======================================")
    print()
    print(
        f"Server: http://{HOST}:{PORT}"
    )
    print(
        "Health: http://127.0.0.1:5000/api/health"
    )
    print()

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )