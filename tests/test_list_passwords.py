from password_manager.model import AuthSession
from password_manager.vault.list_passwords import list_passwords_flow


def test_list_passwords_no_entries(mocker):
    session = AuthSession(user_id=1, username="user", aes_key=b"k")

    # Skip group-selection logic entirely
    mocker.patch(
        "password_manager.vault.list_passwords._select_group",
        return_value=None,
    )

    mocker.patch(
        "password_manager.vault.list_passwords.list_password_entries",
        return_value=[],
    )

    message = mocker.patch(
        "password_manager.vault.list_passwords.MessageScreen.run"
    )

    list_passwords_flow(session)

    message.assert_called_once()
