import pytest
import pyotp
from password_manager.model import AuthSession
from password_manager.auth.login import _verify_2fa
from password_manager.auth.register import _register_user
from password_manager.crypto import derive_aes_key, aes_encrypt, hash_master_password
from password_manager.storage.users import init_users_table, create_user


def test_auth_session_fields():
    session = AuthSession(user_id=1, username="user", aes_key=b"x" * 32)
    assert session.user_id == 1
    assert session.username == "user"


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
        _verify_2fa("missing@test.com", "password")


def test_2fa_success(mocker):
    secret = pyotp.random_base32()
    key = derive_aes_key("password")
    encrypted = aes_encrypt(secret.encode(), key)
    mocker.patch(
        "password_manager.auth.login._input_or_cancel",
        return_value=pyotp.TOTP(secret).now(),
    )
    _verify_2fa(encrypted, key)


def test_2fa_failure(mocker):
    secret = pyotp.random_base32()
    key = derive_aes_key("password")
    encrypted = aes_encrypt(secret.encode(), key)
    mocker.patch(
        "password_manager.auth.login._input_or_cancel",
        return_value="000000",
    )
    with pytest.raises(Exception):
        _verify_2fa(encrypted, key)


def test_register_duplicate_user():
    init_users_table()
    _register_user("dup@test.com", "pass", "pass")
    with pytest.raises(Exception):
        _register_user("dup@test.com", "pass", "pass")
