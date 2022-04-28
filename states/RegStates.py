from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    name_period = State()
    person_type_period = State()
