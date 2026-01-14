from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class PasswordEntry:
    id: int
    user_id: int
    group_id: Optional[int]
    title: str
    service_url: Optional[str]
    account_username: str
    password_encrypted: bytes
    notes: Optional[str]
