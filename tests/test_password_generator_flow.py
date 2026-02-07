from password_manager.vault.password_generator_flow import (
    input_int_with_retry,
    password_generator_flow,
)


def test_input_int_with_retry_default(mocker):
    mocker.patch(
        "password_manager.vault.password_generator_flow.InputScreen.run",
        return_value="",
    )

    value = input_int_with_retry(
        title="Test",
        prompt="Number",
        default=5,
    )

    assert value == 5


def test_password_generator_flow_password(mocker):
    mocker.patch(
        "password_manager.vault.password_generator_flow.Menu.run",
        side_effect=["Password"],
    )

    mocker.patch(
        "password_manager.vault.password_generator_flow.InputScreen.run",
        side_effect=["16", "1", "1", "1", "1"],
    )

    mocker.patch(
        "password_manager.vault.password_generator_flow.generate_password",
        return_value="Abc123!@#",
    )

    view = mocker.patch(
        "password_manager.vault.password_generator_flow.PasswordGenerationViewScreen.run"
    )

    password_generator_flow()

    view.assert_called_once()
