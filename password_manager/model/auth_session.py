from dataclasses import dataclass


@dataclass(slots=True)
class AuthSession:
    user_id: int
    username: str
    aes_key: bytes
