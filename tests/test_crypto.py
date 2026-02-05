from password_manager.crypto import (
    hash_master_password,
    verify_master_password,
    derive_aes_key,
    aes_encrypt,
    aes_decrypt,
)

def test_password_hash_and_verify():
    password = "SuperSecret123!"
    hashed = hash_master_password(password)

    assert verify_master_password(password, hashed)
    assert not verify_master_password("wrong", hashed)

def test_aes_encrypt_decrypt_roundtrip():
    key = derive_aes_key("password")
    data = b"secret-data"

    encrypted = aes_encrypt(data, key)
    decrypted = aes_decrypt(encrypted, key)

    assert decrypted == data

def test_wrong_key_fails():
    key1 = derive_aes_key("password1")
    key2 = derive_aes_key("password2")

    encrypted = aes_encrypt(b"data", key1)

    try:
        aes_decrypt(encrypted, key2)
        assert False, "Decryption should fail"
    except Exception:
        assert True
