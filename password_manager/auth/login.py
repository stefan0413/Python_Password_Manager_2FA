from __future__ import annotations

import pyotp

from .. import crypto
from ..cli import InputScreen, MessageScreen
from ..exceptions import (
    InvalidArgumentException,
    LoginException,
    UserDoesNotExistException,
)
from ..model import AuthSession
from ..storage import users


TITLE_LOGIN = "Login"
TITLE_2FA_VERIFY = "Two-Factor Authentication"

MSG_INVALID_CREDENTIALS = "Invalid username or password."
MSG_INVALID_2FA = "Invalid authentication code."
MSG_AUTH_ERROR = "Authentication error."
MSG_WELCOME = "Welcome, {username}."

PROMPT_USERNAME = "Username"
PROMPT_PASSWORD = "Master password"
PROMPT_2FA_CODE = "Enter 6-digit authenticator code"

def _input_or_cancel(*, title: str, prompt: str, password: bool = False) -> str | None:
    return InputScreen(title=title, prompt=prompt, password=password).run()


def _error(message: str) -> None:
    MessageScreen(title=TITLE_LOGIN, message=message).run()


def _success(message: str) -> None:
    MessageScreen(title=TITLE_LOGIN, message=message, positive=True).run()


def _get_existing_username() -> str:
    username = _input_or_cancel(title=TITLE_LOGIN, prompt=PROMPT_USERNAME)
    if not username:
        raise InvalidArgumentException

    user = users.get_user_with_2fa(username)
    if not user:
        _error(MSG_INVALID_CREDENTIALS)
        raise UserDoesNotExistException

    return username


def _get_and_verify_password(username: str) -> tuple[int, bytes, bytes]:
    user_id, _, password_hash, encrypted_secret = users.get_user_with_2fa(username)

    password = _input_or_cancel(
        title=TITLE_LOGIN,
        prompt=PROMPT_PASSWORD,
        password=True,
    )
    if not password:
        raise InvalidArgumentException

    if not crypto.verify_master_password(password, password_hash):
        _error(MSG_INVALID_CREDENTIALS)
        raise LoginException

    aes_key = crypto.derive_aes_key(password)
    #deleting this so the plain password is not stored in any way
    del password

    return user_id, aes_key, encrypted_secret


def _verify_2fa(encrypted_secret: bytes, aes_key: bytes) -> None:
    code = _input_or_cancel(
        title=TITLE_2FA_VERIFY,
        prompt=PROMPT_2FA_CODE,
    )
    if not code:
        raise InvalidArgumentException

    try:
        secret = crypto.aes_decrypt(encrypted_secret, aes_key).decode()
    except Exception:
        _error(MSG_AUTH_ERROR)
        raise LoginException

    if not pyotp.TOTP(secret).verify(code):
        _error(MSG_INVALID_2FA)
        raise LoginException

def login() -> AuthSession | None:
    try:
        username = _get_existing_username()
        user_id, aes_key, encrypted_secret = _get_and_verify_password(username)
        _verify_2fa(encrypted_secret, aes_key)
    except (LoginException, InvalidArgumentException):
        return None

    _success(MSG_WELCOME.format(username=username))
    return AuthSession(user_id, username, aes_key)
