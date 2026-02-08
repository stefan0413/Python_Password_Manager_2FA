import pytest
from password_manager.crypto import hash_master_password
from password_manager.storage.users import init_users_table, create_user, get_user_with_2fa
from password_manager.storage.groups import init_groups_table, create_group, list_groups
from password_manager.storage.password_entries import (
    init_password_entries_table,
    add_password_entry,
    list_password_entries,
    get_password_entry,
    update_password_entry,
    delete_password_entry,
)


def create_user_id():
    init_users_table()
    return create_user(
        username="test@test.com",
        password_hash=hash_master_password("password"),
        totp_secret=b"secret",
    )


def test_user_create_and_fetch():
    user_id = create_user_id()
    user = get_user_with_2fa("test@test.com")
    assert user[0] == user_id


def test_group_crud():
    user_id = create_user_id()
    init_groups_table()
    create_group(user_id, "Work")
    create_group(user_id, "Personal")
    groups = list_groups(user_id)
    assert [g[1] for g in groups] == ["Personal", "Work"]


def test_password_entry_lifecycle():
    user_id = create_user_id()
    init_groups_table()
    init_password_entries_table()

    add_password_entry(
        user_id=user_id,
        group_id=None,
        title="GitHub",
        service_url=None,
        account_username="user",
        password_encrypted=b"enc",
        notes=None,
    )

    entry_id = list_password_entries(user_id, None)[0][0]

    update_password_entry(
        entry_id,
        user_id,
        None,
        "Updated",
        None,
        "u2",
        b"enc2",
        "note",
    )

    assert get_password_entry(entry_id, user_id).title == "Updated"

    delete_password_entry(entry_id, user_id)
    assert list_password_entries(user_id, None) == []


def test_update_missing_entry():
    with pytest.raises(Exception):
        update_password_entry(999, 1, None, "x", None, "u", b"x", None)
