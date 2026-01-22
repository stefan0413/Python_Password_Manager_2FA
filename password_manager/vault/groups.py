from password_manager.cli import InputScreen, MessageScreen, Menu
from password_manager.exceptions import InvalidArgumentException
from password_manager.storage.groups import create_group, list_groups
from password_manager.model import AuthSession


def create_group_flow(session: AuthSession) -> None:
    name = InputScreen(
        title="Create Group",
        prompt="Group name",
    ).run()

    if not name:
        MessageScreen(
            title="Create Group",
            message="Group name cannot be empty.",
        ).run()
        return

    try:
        create_group(session.user_id, name)
    except InvalidArgumentException:
        MessageScreen(
            title="Create Group",
            message="Group already exists.",
        ).run()
        return

    MessageScreen(
        title="Create Group",
        message=f"Group '{name}' created successfully.",
        positive=True,
    ).run()

def select_group_id_optional(session: AuthSession) -> int | None:
    groups = list_groups(session.user_id)

    if not groups:
        return None

    items = [name for _, name in groups]
    items.append("No group")

    choice = Menu(
        title="Select Group",
        subtitle="Add password entry to a group",
        items=items,
    ).run()

    if not choice or choice == "No group":
        return None

    index = items.index(choice)
    return groups[index][0]
