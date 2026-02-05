from password_manager.model import AuthSession

def test_auth_session_fields():
    session = AuthSession(
        user_id=1,
        username="user",
        aes_key=b"key",
    )

    assert session.user_id == 1
    assert session.username == "user"
