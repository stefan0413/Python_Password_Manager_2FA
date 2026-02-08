import pytest
from password_manager.auth.login import _verify_2fa
from password_manager.crypto import hash_master_password
from password_manager.storage.users import init_users_table, create_user

def test_login_wrong_password():
    init_users_table()

    create_user(
        username="user@test.com",
        password_hash=hash_master_password("correct"),
        totp_secret=b"secret",
    )

    with pytest.raises(Exception):
        _verify_2fa("user@test.com", "wrong")

def test_login_user_not_found():
    with pytest.raises(Exception):
        _verify_2fa("missing@example.com", "password")