import bcrypt
import hashlib


def hash_master_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_master_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)


def derive_aes_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()
