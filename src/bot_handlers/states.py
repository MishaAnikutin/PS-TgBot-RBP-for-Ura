from aiogram.fsm.state import State, StatesGroup


class HandleFileStates(StatesGroup):
    HandleFilesState = State()
    NumberOfCopiesState = State()
    
    