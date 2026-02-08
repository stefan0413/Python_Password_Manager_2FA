import pytest
from password_manager.main import _handle_session, _handle_no_session
from password_manager.model.auth_session import AuthSession
from password_manager.exceptions import UserLogoutException


def test_handle_session_logout(monkeypatch):
    # Fake but valid AES key
    fake_aes_key = b"x" * 32

    session = AuthSession(
        user_id=1,
        username="test",
        aes_key=fake_aes_key,
    )

    # Force menu choice to Logout
    monkeypatch.setattr(
        "password_manager.main.Menu.run",
        lambda self: "Logout"
    )

    with pytest.raises(UserLogoutException):
        _handle_session(session)

def test_handle_no_session_invalid_choice(monkeypatch):
    monkeypatch.setattr(
        "password_manager.main.Menu.run",
        lambda self: "Invalid"
    )

    _handle_no_session()