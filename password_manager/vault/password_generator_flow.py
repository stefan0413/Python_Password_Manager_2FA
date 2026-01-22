from prompt_toolkit.key_binding import KeyBindings

from password_manager.cli import Menu, MessageScreen, InputScreen, PasswordGenerationViewScreen
from password_manager.vault.password_generator import (
    generate_password,
    generate_passphrase,
)
from password_manager.utils.clipboard import copy_to_clipboard

kb = KeyBindings()

def input_int_with_retry(
    *,
    title: str,
    prompt: str,
    default: int,
    min_value: int = 0,
) -> int:
    while True:
        value = InputScreen(
            title=title,
            prompt=f"{prompt} (default: {default})",
        ).run()

        if value is None or value.strip() == "":
            return default

        try:
            number = int(value)
        except ValueError:
            MessageScreen(
                title="Invalid input",
                message=f"{prompt} must be a number.",
            ).run()
            continue

        if number < min_value:
            MessageScreen(
                title="Invalid input",
                message=f"{prompt} must be ≥ {min_value}.",
            ).run()
            continue

        return number


def password_generator_flow() -> None:
    menu = Menu(
        title="Password Generator",
        subtitle="Generate & copy to clipboard",
        items=[
            "Password",
            "Passphrase",
            "Back",
        ],
    )

    choice = menu.run()
    if not choice or choice == "Back":
        return

    if choice == "Password":
        _random_password_flow()
    elif choice == "Passphrase":
        _passphrase_flow()


def _random_password_flow() -> None:
    password: str | None = None

    while True:
        try:
            length = input_int_with_retry(
                title="Password",
                prompt="Length",
                default=16,
                min_value=1,
            )

            min_upper = input_int_with_retry(
                title="Password",
                prompt="Min upper case letters",
                default=1,
            )

            min_lower = input_int_with_retry(
                title="Password",
                prompt="Min lower case letters",
                default=1,
            )

            min_digits = input_int_with_retry(
                title="Password",
                prompt="Min numbers",
                default=1,
            )

            min_symbols = input_int_with_retry(
                title="Password",
                prompt="Min special symbols",
                default=1,
            )

            password = generate_password(
                length,
                min_upper,
                min_lower,
                min_digits,
                min_symbols,
            )

        except ValueError as e:
            MessageScreen(
                title="Invalid password constraints",
                message=str(e),
            ).run()
            continue

        except KeyboardInterrupt:
            return

        break

    PasswordGenerationViewScreen(
            title="Passphrase Generated",
            password=password,
    ).run()

    del password


def _passphrase_flow() -> None:
    passphrase: str | None = None

    while True:
        try:
            words = input_int_with_retry(
                title="Passphrase",
                prompt="Number of words",
                default=4,
                min_value=1,
            )

            passphrase = generate_passphrase(
                words=words,
                capitalize=True,
            )

        except ValueError as e:
            MessageScreen(
                title="Invalid passphrase settings",
                message=str(e),
            ).run()
            continue

        except KeyboardInterrupt:
            return

        break

    PasswordGenerationViewScreen(
        title="Passphrase Generated",
        password = passphrase,
    ).run()

    del passphrase
