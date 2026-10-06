import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

DATABASE_PATH = BASE_DIR / "database" / "trustai.db"


# ---------------------------------------------------------
# SERVER
# ---------------------------------------------------------

HOST = os.getenv(
    "HOST",
    "127.0.0.1"
)

PORT = int(
    os.getenv(
        "PORT",
        "5000"
    )
)

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"


# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "trustai-development-secret-key"
)


# ---------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://127.0.0.1:5500"
)