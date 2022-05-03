from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeRevenuesCategoryStates(StatesGroup):
    new_category_name = State()


class ChangeRevenuesSubCategoryStates(StatesGroup):
    new_sub_category_name = State()


class AddRevenuesCategory(StatesGroup):
    new_category_name = State()


class AddRevenuesSubCategory(StatesGroup):
    new_sub_category_name = State()
