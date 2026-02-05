from password_manager.storage.users import (
    init_users_table,
    create_user,
    get_user_with_2fa,
)
from password_manager.crypto import hash_master_password

def test_create_and_fetch_user():
    init_users_table()

    user_id = create_user(
        username="test@example.com",
        password_hash=hash_master_password("password"),
        totp_secret=b"secret",
    )

    user = get_user_with_2fa("test@example.com")

    assert user is not None
    assert user[0] == user_id
    assert user[1] == "test@example.com"
