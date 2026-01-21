from password_manager.cli import Menu, MessageScreen, InputScreen, PasswordViewScreen
from password_manager.crypto import aes_encrypt, aes_decrypt
from password_manager.password_entry import PasswordEntry
from password_manager.storage.password_entries import (
    list_password_entries,
    get_password_entry,
    update_password_entry,
    delete_password_entry
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

def _edit_password(entry: PasswordEntry, session: AuthSession) -> None:
    title = InputScreen(
        title="Edit Password",
        prompt=f"Title ({entry.title})",
    ).run() or entry.title

    service_url = InputScreen(
        title="Edit Password",
        prompt=f"Service URL ({entry.service_url or 'none'})",
    ).run()
    if service_url == "":
        service_url = entry.service_url

    account_username = InputScreen(
        title="Edit Password",
        prompt=f"Username ({entry.account_username})",
    ).run() or entry.account_username

    new_password = InputScreen(
        title="Edit Password",
        prompt="New password (leave empty to keep current)",
        password=True,
    ).run()

    if new_password:
        encrypted_password = aes_encrypt(
            new_password.encode(),
            session.aes_key,
        )
    else:
        encrypted_password = entry.password_encrypted

    notes = InputScreen(
        title="Edit Password",
        prompt=f"Notes ({entry.notes or 'none'})",
    ).run()
    if notes == "":
        notes = entry.notes

    update_password_entry(
        entry_id=entry.id,
        user_id=session.user_id,
        title=title,
        service_url=service_url,
        account_username=account_username,
        password_encrypted=encrypted_password,
        notes=notes,
    )

    MessageScreen(
        title="Updated",
        message="Password entry updated successfully.",
        positive=True,
    ).run()


def _view_password(entry_id: int, session: AuthSession) -> None:
    entry = get_password_entry(entry_id, session.user_id)
    if not entry:
        MessageScreen(
            title="Error",
            message="Password entry not found.",
        ).run()
        return

    while True:
        menu = Menu(
            title=entry.title,
            subtitle="Password options",
            items=[
                "View",
                "Edit",
                "Delete",
                "Back",
            ],
        )

        choice = menu.run()
        if not choice or choice == "Back":
            break

        if choice == "View":

            plaintext = aes_decrypt(
                    entry.password_encrypted,
                    session.aes_key
            ).decode()

            PasswordViewScreen(
                    title=entry.title,
                    message=(
                        f"Account: {entry.account_username}\n"
                        f"{'-' * 30}\n"
                        f"Password: {plaintext}\n"
                        f"URL: {entry.service_url or 'N/A'}\n"
                        f"Notes:\n{entry.notes or 'N/A'}"
                    ),
                    password=plaintext
            ).run()

            del plaintext

        elif choice == "Edit":
            _edit_password(entry, session)
            break

        elif choice == "Delete":
            confirm = Menu(
                title="Confirm delete",
                subtitle="This action is irreversible",
                items=["Delete", "Cancel"],
            ).run()

            if confirm == "Delete":
                delete_password_entry(entry.id, session.user_id)
                MessageScreen(
                    title="Deleted",
                    message="Password entry deleted.",
                    positive=True,
                ).run()
                break
