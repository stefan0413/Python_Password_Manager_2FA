from .users import init_users_table
from .groups import init_groups_table
from .password_entries import init_password_entries_table

def init_db():
    init_users_table()
    init_groups_table()
    init_password_entries_table()
