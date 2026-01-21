from password_manager.cli import Menu, MessageScreen
from password_manager.crypto import aes_decrypt
from password_manager.storage.password_entries import (
    list_password_entries,
    get_password_entry,
)
from password_manager.model import AuthSession


def list_passwords_flow(session: AuthSession) -> None:
    rows = list_password_entries(session.user_id)

    if not rows:
        MessageScreen(
            title="Passwords",
            message="No passwords saved yet."
        ).run()
        return

    items = [
        f"{title} ({username})"
        for _, title, username in rows
    ]
    items.append("Back")

    menu = Menu(
        title="Passwords",
        subtitle="Select an entry to view",
        items=items,
    )

    choice = menu.run()
    if not choice or choice == "Back":
        return

    index = items.index(choice)
    entry_id = rows[index][0]

    _view_password(entry_id, session)


def _view_password(entry_id: int, session: AuthSession) -> None:
    entry = get_password_entry(entry_id, session.user_id)
    if not entry:
        MessageScreen(
            title="Error",
            message="Password entry not found."
        ).run()
        return

    plaintext = aes_decrypt(
        entry.password_encrypted,
        session.aes_key
    ).decode()

    MessageScreen(
        title=entry.title,
        message=f"Username: {entry.account_username}\n\nPassword:\n{plaintext}",
        positive=True
    ).run()

    del plaintext
