import sqlite3
import sys
from pathlib import Path

# Allow importing config when running app.py
BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from backend.config import DATABASE_PATH


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        str(DATABASE_PATH)
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password TEXT NOT NULL,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------------------------------
    # ANALYSES
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            domain TEXT NOT NULL,

            prediction TEXT NOT NULL,

            predicted_value REAL,

            risk_level TEXT NOT NULL,

            confidence INTEGER DEFAULT 0,

            trust_score INTEGER DEFAULT 0,

            input_data TEXT,

            explanation TEXT,

            recommendation TEXT,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    # -----------------------------------------------------
    # SETTINGS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL UNIQUE,

            notifications INTEGER DEFAULT 1,

            email_alerts INTEGER DEFAULT 1,

            dark_mode INTEGER DEFAULT 0,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_database()

    print("TrustAI database created successfully.")