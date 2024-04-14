from aiogram.fsm.state import State, StatesGroup


class MailingStates(StatesGroup):
    GetMailingMessageState = State()
    SendAllUsersState = State()
        