
from . import storage, crypto
from .cli import InputScreen, MessageScreen

import pyotp
import qrcode



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

    if storage.get_user_with_2fa(username):
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
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)

    aes_key = crypto.derive_aes_key(password)
    totp_secret = crypto.aes_encrypt(secret.encode(), aes_key)

    user_id = storage.create_user(username, password_hash, totp_secret)
    uri = totp.provisioning_uri(
        name=username,
        issuer_name="Console Password Manager"
    )

    qr = qrcode.QRCode()
    qr.add_data(uri)
    qr.make()

    print("\nScan this QR code with Google Authenticator:\n")
    qr.print_ascii()
    input("\nPress Enter after scanning...")

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

    user = storage.get_user_with_2fa(username)

    if not user:
        MessageScreen(
            title="Login Failed",
            message="Invalid username or password."
        ).run()
        return None

    user_id, _, password_hash, encrypted_secret = user

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

    code = InputScreen(
        title="Two-Factor Authentication",
        prompt="Enter 6-digit authenticator code"
    ).run()

    if not code:
        return None

    aes_key = crypto.derive_aes_key(password)

    try:
        secret = crypto.aes_decrypt(encrypted_secret, aes_key).decode()
    except Exception:
        MessageScreen(
            title="Login Failed",
            message="Authentication error."
        ).run()
        return None

    totp = pyotp.TOTP(secret)

    if not totp.verify(code):
        MessageScreen(
            title="Login Failed",
            message="Invalid authentication code."
        ).run()
        return None

    MessageScreen(
        title="Welcome",
        message=f"Welcome, {username}.",
        positive=True
    ).run()

    return AuthSession(user_id, username, aes_key)
