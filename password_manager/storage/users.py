from datetime import datetime, timezone
from password_manager.storage.db import db

SQL_CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash BLOB NOT NULL,
        totp_secret BLOB NOT NULL,
        created_at TEXT NOT NULL
    );
"""

SQL_INSERT_USER = """
    INSERT INTO users (username, password_hash, totp_secret, created_at)
    VALUES (?, ?, ?, ?)
"""

SQL_SELECT_USER_WITH_2FA = """
    SELECT id, username, password_hash, totp_secret
    FROM users
    WHERE username = ?
"""

def init_users_table():
    with db() as conn:
        conn.execute(SQL_CREATE_USERS_TABLE)

def create_user(username: str, password_hash: bytes, totp_secret: bytes):
    with db() as conn:
        cursor = conn.execute(
            SQL_INSERT_USER,
            (username, password_hash, totp_secret,
             datetime.now(timezone.utc).isoformat())
        )
        return cursor.lastrowid

def get_user_with_2fa(username: str):
    with db() as conn:
        cursor = conn.execute(SQL_SELECT_USER_WITH_2FA, (username,))
        return cursor.fetchone()
