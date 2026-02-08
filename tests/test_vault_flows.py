from password_manager.model import AuthSession
from password_manager.vault.add_password import add_password_flow
from password_manager.vault.groups import create_group_flow, select_group_id_optional
from password_manager.vault.list_passwords import list_passwords_flow


def session():
    return AuthSession(user_id=1, username="user", aes_key=b"x" * 32)


def test_add_password_flow(mocker):
    mocker.patch(
        "password_manager.vault.add_password.InputScreen.run",
        side_effect=["Title", "user", "pass", "", ""],
    )
    mocker.patch("password_manager.vault.add_password.select_group_id_optional", return_value=None)
    mocker.patch("password_manager.vault.add_password.aes_encrypt", return_value=b"x")
    mocker.patch("password_manager.vault.add_password.add_password_entry")
    message = mocker.patch("password_manager.vault.add_password.MessageScreen.run")
    add_password_flow(session())
    message.assert_called_once()


def test_group_flow_create(mocker):
    mocker.patch("password_manager.vault.groups.InputScreen.run", return_value="Work")
    mocker.patch("password_manager.vault.groups.create_group")
    message = mocker.patch("password_manager.vault.groups.MessageScreen.run")

    create_group_flow(session())

    message.assert_called()


def test_group_select_none(monkeypatch):
    monkeypatch.setattr("password_manager.vault.groups.list_groups", lambda _: [])
    assert select_group_id_optional(session()) is None


def test_list_passwords_empty(mocker):
    mocker.patch("password_manager.vault.list_passwords._select_group", return_value=None)
    mocker.patch("password_manager.vault.list_passwords.list_password_entries", return_value=[])
    message = mocker.patch("password_manager.vault.list_passwords.MessageScreen.run")
    list_passwords_flow(session())
    message.assert_called_once()
