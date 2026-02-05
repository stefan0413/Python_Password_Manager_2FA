import pytest
from password_manager.vault.password_generator import (
    generate_password,
    generate_passphrase,
)

def test_generate_password_length():
    pwd = generate_password(length=20)
    assert len(pwd) == 20

def test_generate_password_constraints():
    pwd = generate_password(
        length=10,
        min_upper=2,
        min_lower=2,
        min_digits=2,
        min_symbols=2,
    )

    assert sum(c.isupper() for c in pwd) >= 2
    assert sum(c.islower() for c in pwd) >= 2
    assert sum(c.isdigit() for c in pwd) >= 2

def test_invalid_constraints():
    with pytest.raises(ValueError):
        generate_password(length=3, min_upper=2, min_lower=2)

def test_generate_passphrase():
    phrase = generate_passphrase(words=4)
    assert len(phrase.split("-")) == 4
