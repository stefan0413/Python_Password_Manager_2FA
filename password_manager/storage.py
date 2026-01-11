import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "password_manager.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            totp_secret BLOB NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_user(username: str, password_hash: bytes, totp_secret: bytes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password_hash, created_at, totp_secret) VALUES (?, ?, ?, ?)",
        (username, password_hash, datetime.utcnow().isoformat(), totp_secret)
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id

def get_user_with_2fa(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, totp_secret FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user
