from password_manager.exceptions import GracefulShutdownException, UserLogoutException
from password_manager.model import AuthSession
from password_manager.storage import init_db
from password_manager.vault.add_password import add_password_flow
from password_manager.vault.list_passwords import list_passwords_flow
from . import auth
from .cli import Menu

def _exit_if_chosen(choice: str) -> None:
    if choice == "Exit" or choice is None:
        raise GracefulShutdownException

def _handle_no_session()-> AuthSession | None:
    menu = Menu(
            title="PASSWORD MANAGER",
            subtitle="Secure • Offline • Encrypted",
            items=[
                "Register",
                "Login",
                "Exit",
            ],
    )

    choice = menu.run()

    if choice == "Register":
        auth.register()
        return None

    elif choice == "Login":
        return auth.login()

    _exit_if_chosen(choice)

    return None

def _handle_session (session: AuthSession) -> None:
    menu = Menu(
            title=f"Welcome, {session.username}",
            subtitle="Vault unlocked",
            items=[
                "Add password",
                "List passwords",
                "Logout",
                "Exit",
            ],
    )

    print(f"Session {session.username} {session.user_id} {session.aes_key}")

    choice = menu.run()

    if choice == "Add password":
        add_password_flow(session)
    elif choice == "List passwords":
        list_passwords_flow(session)
    elif choice == "Logout":
        raise UserLogoutException

    _exit_if_chosen(choice)

def main():
    init_db()

    session = None
    running = True

    try:
        while running:
            if session is None:
               session = _handle_no_session()
            else:
                try:
                    _handle_session(session)
                except UserLogoutException:
                    session = None
    except (KeyboardInterrupt, GracefulShutdownException):
        pass

if __name__ == "__main__":
    main()
