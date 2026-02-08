import pytest
from password_manager.crypto import (
    hash_master_password,
    verify_master_password,
    derive_aes_key,
    aes_encrypt,
    aes_decrypt,
)


def test_password_hash_and_verify():
    hashed = hash_master_password("secret")
    assert verify_master_password("secret", hashed)
    assert not verify_master_password("wrong", hashed)


def test_aes_roundtrip():
    key = derive_aes_key("password")
    data = b"data"
    assert aes_decrypt(aes_encrypt(data, key), key) == data


def test_aes_wrong_key():
    encrypted = aes_encrypt(b"x", derive_aes_key("a"))
    with pytest.raises(Exception):
        aes_decrypt(encrypted, derive_aes_key("b"))
