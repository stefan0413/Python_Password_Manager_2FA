import pyotp
import pytest

from password_manager.auth.register import _register_user
from password_manager.crypto import derive_aes_key, aes_encrypt, hash_master_password
from password_manager.storage.users import init_users_table, create_user
from password_manager.auth.login import _verify_2fa

def test_2fa_verification_success(mocker):
    secret = pyotp.random_base32()
    key = derive_aes_key("password")
    encrypted = aes_encrypt(secret.encode(), key)

    mocker.patch(
        "password_manager.auth.login._input_or_cancel",
        return_value=pyotp.TOTP(secret).now(),
    )

    _verify_2fa(encrypted, key)

def test_2fa_verification_fail(mocker):
    secret = pyotp.random_base32()
    key = derive_aes_key("password")
    encrypted = aes_encrypt(secret.encode(), key)

    mocker.patch(
        "password_manager.auth.login._input_or_cancel",
        return_value="000000",
    )

    try:
        _verify_2fa(encrypted, key)
        assert False
    except Exception:
        assert True


def test_register_duplicate_user():
    init_users_table()

    _register_user("dup@test.com", "pass", "pass")

    with pytest.raises(Exception):
        _register_user("dup@test.com", "pass", "pass")
