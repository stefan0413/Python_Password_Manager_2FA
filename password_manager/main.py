from . import storage, auth
from .cli import Menu


def main():
    # Initialize database
    storage.init_db()

    session = None
    running = True

    try:
        while running:
            # =========================
            # NOT LOGGED IN
            # =========================
            if session is None:
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

                elif choice == "Login":
                    session = auth.login()

                elif choice == "Exit" or choice is None:
                    running = False

            # =========================
            # LOGGED IN
            # =========================
            else:
                menu = Menu(
                    title=f"Welcome, {session.username}",
                    subtitle="Vault unlocked",
                    items=[
                        "Logout",
                        "Exit",
                    ],
                )

                choice = menu.run()

                if choice == "Logout":
                    session = None

                elif choice == "Exit" or choice is None:
                    running = False
    except KeyboardInterrupt:
        print("\nExiting...")

    # Clean exit (session automatically destroyed)
    print("Goodbye.")


if __name__ == "__main__":
    main()
