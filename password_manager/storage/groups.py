from datetime import datetime, timezone
from db import db

SQL_CREATE_GROUPS_TABLE = """
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE (user_id, name)
    );
"""

def init_groups_table():
    with db() as conn:
        conn.execute(SQL_CREATE_GROUPS_TABLE)

def create_group(user_id: int, name: str):
    with db() as conn:
        conn.execute(
            "INSERT INTO groups (user_id, name, created_at) VALUES (?, ?, ?)",
            (user_id, name, datetime.now(timezone.utc).isoformat()))

def list_groups(user_id: int):
    with db() as conn:
        return conn.execute(
            "SELECT id, name FROM groups WHERE user_id = ? ORDER BY name",
            (user_id,)
        ).fetchall()
