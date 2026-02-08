from password_manager.model import AuthSession
from password_manager.storage import init_groups_table
from password_manager.storage.groups import list_groups
from password_manager.vault.groups import (
    create_group_flow,
    select_group_id_optional,
)


def test_create_group_flow_success(mocker):
    session = AuthSession(user_id=1, username="user", aes_key=b"k")

    mocker.patch(
        "password_manager.vault.groups.InputScreen.run",
        return_value="Work",
    )

    create_group = mocker.patch(
        "password_manager.vault.groups.create_group"
    )

    message = mocker.patch(
        "password_manager.vault.groups.MessageScreen.run"
    )

    create_group_flow(session)

    create_group.assert_called_once_with(1, "Work")
    message.assert_called()


def test_select_group_id_optional_choice(mocker):
    session = AuthSession(user_id=1, username="user", aes_key=b"k")

    mocker.patch(
        "password_manager.vault.groups.list_groups",
        return_value=[(1, "Work"), (2, "Personal")],
    )

    mocker.patch(
        "password_manager.vault.groups.Menu.run",
        return_value="Personal",
    )

    group_id = select_group_id_optional(session)

    assert group_id == 2

def test_list_groups_empty():
    init_groups_table()
    assert list_groups(user_id=999) == []