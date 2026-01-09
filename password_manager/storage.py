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
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_user(username: str, password_hash: bytes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user
