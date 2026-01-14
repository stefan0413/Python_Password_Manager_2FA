import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "password_manager.db"

PRAGMA_FOREIGN_KEYS = "PRAGMA foreign_keys = ON"

@contextmanager
def db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(PRAGMA_FOREIGN_KEYS)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
