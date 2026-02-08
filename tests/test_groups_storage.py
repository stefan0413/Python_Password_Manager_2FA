from password_manager.exceptions import InvalidArgumentException
from password_manager.model import AuthSession
from password_manager.storage.users import init_users_table, create_user
from password_manager.storage.groups import init_groups_table, create_group, list_groups
from password_manager.crypto import hash_master_password
from password_manager.vault.groups import select_group_id_optional, create_group_flow


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


def test_select_group_id_optional_empty(monkeypatch):
    session = AuthSession(
        user_id=1,
        username="test",
        aes_key=b"x" * 32,
    )

    # Patch the storage dependency used inside the flow
    monkeypatch.setattr(
        "password_manager.vault.groups.list_groups",
        lambda user_id: []
    )

    result = select_group_id_optional(session)

    assert result is None

def test_select_group_id_optional_with_group(monkeypatch):
    session = AuthSession(
        user_id=1,
        username="test",
        aes_key=b"x" * 32,
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.list_groups",
        lambda user_id: [(5, "Work"), (6, "Personal")]
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.Menu.run",
        lambda self: "Work"
    )

    result = select_group_id_optional(session)

    assert result == 5

def test_create_group_flow_empty_name(monkeypatch):
    session = AuthSession(
        user_id=1,
        username="test",
        aes_key=b"x" * 32,
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.InputScreen.run",
        lambda self: ""
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.MessageScreen.run",
        lambda self: None
    )

    create_group_flow(session)

def test_create_group_flow_duplicate(monkeypatch):
    session = AuthSession(
        user_id=1,
        username="test",
        aes_key=b"x" * 32,
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.InputScreen.run",
        lambda self: "Work"
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.create_group",
        lambda user_id, name: (_ for _ in ()).throw(InvalidArgumentException())
    )

    monkeypatch.setattr(
        "password_manager.vault.groups.MessageScreen.run",
        lambda self: None
    )

    create_group_flow(session)