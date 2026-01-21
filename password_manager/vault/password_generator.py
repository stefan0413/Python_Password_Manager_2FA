import random
import string
from wordfreq import top_n_list


def generate_password(
    length: int = 16,
    min_upper: int = 1,
    min_lower: int = 1,
    min_digits: int = 1,
    min_symbols: int = 1,
) -> str:
    if length <= 0:
        raise ValueError("Password length must be positive.")

    for name, value in {
        "min_upper": min_upper,
        "min_lower": min_lower,
        "min_digits": min_digits,
        "min_symbols": min_symbols,
    }.items():
        if value < 0:
            raise ValueError(f"{name} cannot be negative.")

    if min_upper == min_lower == min_digits == min_symbols == 0:
        raise ValueError(
            "At least one character category must have a minimum greater than 0."
        )

    required = min_upper + min_lower + min_digits + min_symbols
    if required > length:
        raise ValueError(
            f"Invalid constraints: minimum required characters "
            f"({required}) exceed password length ({length})."
        )

    password_chars: list[str] = []

    password_chars += random.choices(string.ascii_uppercase, k=min_upper)
    password_chars += random.choices(string.ascii_lowercase, k=min_lower)
    password_chars += random.choices(string.digits, k=min_digits)
    password_chars += random.choices(string.punctuation, k=min_symbols)

    remaining = length - len(password_chars)
    if remaining > 0:
        all_chars = (
            string.ascii_letters +
            string.digits +
            string.punctuation
        )
        password_chars += random.choices(all_chars, k=remaining)

    random.shuffle(password_chars)

    return "".join(password_chars)

WORDLIST = top_n_list("en", 5000)

def _validate_passphrase(words, separator) -> None:
    if words <= 0:
        raise ValueError("Number of words must be greater than 0.")

    if not isinstance(separator, str):
        raise ValueError("Separator must be a string.")

    if separator == "":
        raise ValueError("Separator cannot be empty.")

    if not WORDLIST:
        raise ValueError("Wordlist is empty.")

def generate_passphrase(
    words: int = 4,
    separator: str = "-",
    capitalize: bool = False,
) -> str:
    _validate_passphrase(words, separator)
    chosen = random.choices(WORDLIST, k=words)

    if capitalize:
        chosen = [w.capitalize() for w in chosen]

    return separator.join(chosen)
