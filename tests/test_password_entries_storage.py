from password_manager.storage.users import init_users_table, create_user
from password_manager.storage.groups import init_groups_table
from password_manager.storage.password_entries import (
    init_password_entries_table,
    add_password_entry,
    list_password_entries,
    get_password_entry,
    update_password_entry,
    delete_password_entry,
)
from password_manager.crypto import hash_master_password


def test_password_entry_lifecycle():
    # FK dependency order: users → groups → password_entries
    init_users_table()
    init_groups_table()
    init_password_entries_table()

    user_id = create_user(
        username="test@example.com",
        password_hash=hash_master_password("password"),
        totp_secret=b"secret",
    )

    add_password_entry(
        user_id=user_id,
        group_id=None,
        title="GitHub",
        service_url="https://github.com",
        account_username="user",
        password_encrypted=b"encrypted",
        notes=None,
    )

    entries = list_password_entries(user_id, None)
    assert len(entries) == 1

    entry_id = entries[0][0]

    entry = get_password_entry(entry_id, user_id)
    assert entry.title == "GitHub"

    update_password_entry(
        entry_id=entry_id,
        user_id=user_id,
        group_id=None,
        title="GitHub Updated",
        service_url=None,
        account_username="user2",
        password_encrypted=b"enc2",
        notes="note",
    )

    updated = get_password_entry(entry_id, user_id)
    assert updated.title == "GitHub Updated"

    delete_password_entry(entry_id, user_id)
    assert list_password_entries(user_id, None) == []
