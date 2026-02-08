import pytest
from password_manager.vault.password_generator import generate_password, generate_passphrase
from password_manager.vault.password_generator_flow import input_int_with_retry, password_generator_flow


def test_generate_password_constraints():
    pwd = generate_password(12, 2, 2, 2, 2)
    assert len(pwd) == 12


def test_generate_password_invalid():
    with pytest.raises(ValueError):
        generate_password(0)


def test_generate_passphrase():
    assert len(generate_passphrase(4).split("-")) == 4


def test_input_int_default(mocker):
    mocker.patch(
        "password_manager.vault.password_generator_flow.InputScreen.run",
        return_value="",
    )

    value = input_int_with_retry(
        title="T",
        prompt="P",
        default=5,
    )

    assert value == 5



def test_password_generator_flow(mocker):
    mocker.patch("password_manager.vault.password_generator_flow.Menu.run", return_value="Password")
    mocker.patch(
        "password_manager.vault.password_generator_flow.InputScreen.run",
        side_effect=["12", "1", "1", "1", "1"],
    )
    mocker.patch(
        "password_manager.vault.password_generator_flow.generate_password",
        return_value="Abc123!",
    )
    view = mocker.patch(
        "password_manager.vault.password_generator_flow.PasswordGenerationViewScreen.run"
    )
    password_generator_flow()
    view.assert_called_once()
