from password_manager.storage.users import init_users_table, create_user
from password_manager.storage.groups import init_groups_table, create_group, list_groups
from password_manager.crypto import hash_master_password

def test_group_crud():
    # init dependencies
    init_users_table()
    init_groups_table()

    user_id = create_user(
        username="test@example.com",
        password_hash=hash_master_password("password"),
        totp_secret=b"secret",
    )

    create_group(user_id=user_id, name="Work")
    create_group(user_id=user_id, name="Personal")

    groups = list_groups(user_id)

    assert len(groups) == 2
    assert [name for _, name in groups] == ["Personal", "Work"]
