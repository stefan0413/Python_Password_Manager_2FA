from password_manager.storage.db import db
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
                SELECT id, user_id, group_id, title,
                       service_url, account_username,
                       password_encrypted, notes
                FROM password_entries
                WHERE id = ? AND user_id = ?
            """,
            (entry_id, user_id)
        ).fetchone()

    if row is None:
        return None

    return PasswordEntry(*row)

def list_password_entries(
    user_id: int,
    group_id: int | None,
) -> list[tuple[int, str, str]]:

    params: list[int] = [user_id]
    group_select_query = ""

    if group_id is not None:
        group_select_query = " AND group_id = ?"
        params.append(group_id)

    with db() as conn:
        rows = conn.execute(
            f"""
            SELECT id, title, account_username
            FROM password_entries
            WHERE user_id = ?{group_select_query}
            ORDER BY created_at DESC
            """,
            tuple(params),
        ).fetchall()

    return rows


def update_password_entry(
    entry_id: int,
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
            UPDATE password_entries
            SET group_id = ?,
                title = ?,
                service_url = ?,
                account_username = ?,
                password_encrypted = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (
                group_id,
                title,
                service_url,
                account_username,
                password_encrypted,
                notes,
                entry_id,
                user_id,
            )
        )

def delete_password_entry(entry_id: int, user_id: int) -> None:
    with db() as conn:
        conn.execute(
            "DELETE FROM password_entries WHERE id = ? AND user_id = ?",
            (entry_id, user_id),
        )
