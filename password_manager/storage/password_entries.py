from db import db
from password_manager.password_entry import PasswordEntry


SQL_CREATE_PASSWORD_ENTRIES_TABLE = """
    CREATE TABLE IF NOT EXISTS password_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        group_id INTEGER,
        title TEXT NOT NULL,
        service_url TEXT,
        account_username TEXT NOT NULL,
        password_encrypted BLOB NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE SET NULL
    );
"""

def init_password_entries_table():
    with db() as conn:
        conn.execute(SQL_CREATE_PASSWORD_ENTRIES_TABLE)

def add_password_entry(
    user_id: int,
    group_id: int | None,
    title: str,
    service_url: str | None,
    account_username: str,
    password_encrypted: bytes,
    notes: str | None,
) -> None:
    with db() as conn:
        conn.execute(
            """
            INSERT INTO password_entries
            (user_id, group_id, title, service_url,
             account_username, password_encrypted, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, group_id, title, service_url,
             account_username, password_encrypted, notes)
        )

def get_password_entry(entry_id: int, user_id: int) -> PasswordEntry | None:
    with db() as conn:
        row = conn.execute(
            """
            SELECT id,
                   user_id,
                   group_id,
                   title,
                   service_url,
                   account_username,
                   password_encrypted,
                   notes
            FROM password_entries
            WHERE id = ?
              AND user_id = ?
            """,
            (entry_id, user_id)
        ).fetchone()

    if row is None:
        return None

    return PasswordEntry(*row)