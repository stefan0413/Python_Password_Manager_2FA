import tempfile
import os
import pytest
from pathlib import Path

@pytest.fixture(autouse=True)
def isolated_db(monkeypatch):
    from password_manager.storage import db as db_module

    tmpdir = tempfile.TemporaryDirectory()
    test_db = Path(tmpdir.name) / "test.db"

    monkeypatch.setattr(db_module, "DB_PATH", test_db)

    yield
    tmpdir.cleanup()
