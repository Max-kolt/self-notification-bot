from aiogram.fsm.state import StatesGroup, State


class AddNote(StatesGroup):
    text = State()
    date = State()
    time = State()
