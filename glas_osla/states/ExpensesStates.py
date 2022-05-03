from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeExpensesCategoryStates(StatesGroup):
    new_category_name = State()


class ChangeExpensesSubCategoryStates(StatesGroup):
    new_sub_category_name = State()
