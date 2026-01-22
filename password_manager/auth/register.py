from __future__ import annotations
import re
import pyotp

from .. import crypto
from ..cli import InputScreen, MessageScreen, QrCodeScreen
from ..exceptions import (
    InvalidArgumentException,
    RegistrationException,
    UserAlreadyExistsException,
    PasswordsDoNotMatch,
)
from ..storage import users


TITLE_REGISTER = "Register"
TITLE_2FA_SETUP = "Two-Factor Authentication Setup"

MSG_USER_EXISTS = "User already exists."
MSG_PASSWORD_MISMATCH = "Passwords do not match."
MSG_REGISTER_SUCCESS = "User registered successfully."
MSG_INVALID_USERNAME = "Invalid username. \nUsername shall be a valid email address."

PROMPT_USERNAME = "Username"
PROMPT_PASSWORD = "Master password"
PROMPT_CONFIRM_PASSWORD = "Confirm master password"

ISSUER_NAME = "Console Password Manager"
EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def _input_or_cancel(*, title: str, prompt: str, password: bool = False) -> str | None:
    return InputScreen(title=title, prompt=prompt, password=password).run()


def _error(message: str) -> None:
    MessageScreen(title=TITLE_REGISTER, message=message).run()


def _success(message: str) -> None:
    MessageScreen(title=TITLE_REGISTER, message=message, positive=True).run()


def _validate_new_username(username: str | None) -> None:
    if not username:
        raise InvalidArgumentException

    if users.get_user_with_2fa(username):
        _error(MSG_USER_EXISTS)
        raise UserAlreadyExistsException

    if not is_valid_email(username):
        _error(MSG_INVALID_USERNAME)
        raise InvalidArgumentException

def _get_new_username() -> str:
    username = _input_or_cancel(title=TITLE_REGISTER, prompt=PROMPT_USERNAME)
    _validate_new_username(username)
    return username


def _get_and_confirm_password() -> str:
    password = _input_or_cancel(
            title=TITLE_REGISTER,
            prompt=PROMPT_PASSWORD,
            password=True,
    )
    if not password:
        raise InvalidArgumentException

    confirm = _input_or_cancel(
            title=TITLE_REGISTER,
            prompt=PROMPT_CONFIRM_PASSWORD,
            password=True,
    )

    if password != confirm:
        _error(MSG_PASSWORD_MISMATCH)
        raise PasswordsDoNotMatch

    return password


def _register_user(username: str, password: str, secret_2fa: str) -> None:
    aes_key = crypto.derive_aes_key(password)
    encrypted_secret = crypto.aes_encrypt(secret_2fa.encode(), aes_key)
    password_hash = crypto.hash_master_password(password)

    users.create_user(username, password_hash, encrypted_secret)


def _show_2fa_qr_code(username: str, secret_2fa: str) -> None:
    totp = pyotp.TOTP(secret_2fa)
    uri = totp.provisioning_uri(name=username, issuer_name=ISSUER_NAME)

    QrCodeScreen(
            title=TITLE_2FA_SETUP,
            uri=uri,
            secret=secret_2fa,
    ).run()


def register() -> None:
    while True:
        try:
            username = _get_new_username()
            password = _get_and_confirm_password()
            break

        except (RegistrationException, InvalidArgumentException):
            pass

    secret_2fa = pyotp.random_base32()

    _register_user(username, password, secret_2fa)
    _show_2fa_qr_code(username, secret_2fa)
    _success(MSG_REGISTER_SUCCESS)
