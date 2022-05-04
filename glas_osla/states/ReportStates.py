from aiogram.dispatcher.filters.state import State, StatesGroup


class EnterDateStates(StatesGroup):
    new_date = State()
