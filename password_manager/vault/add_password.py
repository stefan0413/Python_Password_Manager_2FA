from password_manager.cli import InputScreen, MessageScreen
from password_manager.crypto import aes_encrypt
from password_manager.exceptions import InvalidArgumentException
from password_manager.storage.password_entries import add_password_entry
from password_manager.model import AuthSession


def _input_field(prompt: str, password: bool = False) -> str:
    screen = InputScreen(
        title="Add Password",
        prompt=prompt,
        password=password
    )

    value = screen.run()

    if not value:
        raise InvalidArgumentException

    return value

def add_password_flow(session: AuthSession) -> None:
    title = _input_field("Title (e.g. GitHub)")
    service_url = _input_field("Service URL (optional)")
    account_username = _input_field("Account Username")
    plaintext_password = _input_field("Account Password", True)

    notes = _input_field("Notes")

    encrypted_password = aes_encrypt(
        plaintext_password.encode(),
        session.aes_key
    )

    add_password_entry(
        user_id=session.user_id,
        group_id=None,
        title=title,
        service_url=service_url,
        account_username=account_username,
        password_encrypted=encrypted_password,
        notes=notes,
    )

    del plaintext_password

    MessageScreen(
        title="Add Password",
        message="Password saved successfully.",
        positive=True
    ).run()
