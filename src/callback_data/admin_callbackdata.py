from enum import Enum


class AdminCallback(str, Enum):
    Mailing = 'mailing'
    CountUsers = 'count_users'
    Reset = 'admin:reset'

