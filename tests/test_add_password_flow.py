import pytest
from password_manager.model import AuthSession
from password_manager.vault.add_password import add_password_flow


def test_add_password_flow_success(mocker):
    session = AuthSession(
        user_id=1,
        username="user",
        aes_key=b"key",
    )

    # Mock user inputs (title, username, password, url, notes)
    mocker.patch(
        "password_manager.vault.add_password.InputScreen.run",
        side_effect=[
            "GitHub",        # title
            "user",          # account username
            "Password123!",  # password
            "",              # service_url
            "",              # notes
        ],
    )

    mocker.patch(
        "password_manager.vault.add_password.select_group_id_optional",
        return_value=None,
    )

    encrypt = mocker.patch(
        "password_manager.vault.add_password.aes_encrypt",
        return_value=b"encrypted",
    )

    add_entry = mocker.patch(
        "password_manager.vault.add_password.add_password_entry"
    )

    message = mocker.patch(
        "password_manager.vault.add_password.MessageScreen.run"
    )

    add_password_flow(session)

    encrypt.assert_called_once()
    add_entry.assert_called_once()
    message.assert_called_once()
