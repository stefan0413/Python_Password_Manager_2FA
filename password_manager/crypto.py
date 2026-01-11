import base64

import bcrypt
import hashlib

from cryptography.fernet import Fernet


def hash_master_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_master_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)


def derive_aes_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.encrypt(data)


def aes_decrypt(token: bytes, key: bytes) -> bytes:
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.decrypt(token)
