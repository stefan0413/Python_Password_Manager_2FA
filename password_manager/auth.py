# password_manager/auth.py

from . import storage, crypto
from .cli import InputScreen, MessageScreen


class AuthSession:
    def __init__(self, user_id: int, username: str, aes_key: bytes):
        self.user_id = user_id
        self.username = username
        self.aes_key = aes_key


def register():
    username = InputScreen(
        title="Register",
        prompt="Username"
    ).run()

    if not username:
        return

    if storage.get_user_by_username(username):
        MessageScreen(
            title="Registration Error",
            message="User already exists."
        ).run()
        return

    password = InputScreen(
        title="Register",
        prompt="Master password",
        password=True
    ).run()

    if not password:
        return

    confirm = InputScreen(
        title="Register",
        prompt="Confirm master password",
        password=True
    ).run()

    if password != confirm:
        MessageScreen(
            title="Registration Error",
            message="Passwords do not match."
        ).run()
        return

    password_hash = crypto.hash_master_password(password)
    storage.create_user(username, password_hash)

    MessageScreen(
        title="Success",
        message="User registered successfully.",
        positive=True
    ).run()


def login() -> AuthSession | None:
    username = InputScreen(
        title="Login",
        prompt="Username"
    ).run()

    if not username:
        return None

    user = storage.get_user_by_username(username)
    if not user:
        MessageScreen(
            title="Login Failed",
            message="Invalid username or password."
        ).run()
        return None

    user_id, _, password_hash = user

    password = InputScreen(
        title="Login",
        prompt="Master password",
        password=True
    ).run()

    if not password:
        return None

    if not crypto.verify_master_password(password, password_hash):
        MessageScreen(
            title="Login Failed",
            message="Invalid username or password."
        ).run()
        return None

    aes_key = crypto.derive_aes_key(password)

    MessageScreen(
        title="Welcome",
        message=f"Welcome, {username}.",
        positive=True
    ).run()

    return AuthSession(user_id, username, aes_key)
