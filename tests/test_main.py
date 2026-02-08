import pytest
from password_manager.main import main, _handle_session, _handle_no_session
from password_manager.exceptions import UserLogoutException
from password_manager.model import AuthSession


def test_main_exit(monkeypatch):
    monkeypatch.setattr("password_manager.main.Menu.run", lambda self: "Exit")
    monkeypatch.setattr("password_manager.main.clear", lambda: None)
    main()


def test_handle_session_logout(monkeypatch):
    monkeypatch.setattr("password_manager.main.Menu.run", lambda self: "Logout")

    session = AuthSession(
        user_id=1,
        username="user",
        aes_key=b"x" * 32,
    )

    with pytest.raises(UserLogoutException):
        _handle_session(session)


def test_handle_no_session_invalid(monkeypatch):
    monkeypatch.setattr("password_manager.main.Menu.run", lambda self: "Invalid")
    _handle_no_session()
