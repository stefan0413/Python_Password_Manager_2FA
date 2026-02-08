# tests/test_main.py
import pytest
from password_manager import main
from password_manager.exceptions import GracefulShutdownException


def test_main_exit_immediately(monkeypatch):
    # Force Menu.run() to return "Exit" immediately
    monkeypatch.setattr(
        "password_manager.main.Menu.run",
        lambda self: "Exit"
    )

    # Prevent clearing terminal from causing side effects
    monkeypatch.setattr(
        "password_manager.main.clear",
        lambda: None
    )

    # main() should exit cleanly
    main.main()
