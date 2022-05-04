from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from glas_osla.db.db_commands import (
    get_user_categories, get_user_categories,
    get_user_subcategories
)
from glas_osla.db.models.expenses_plots_md import ExpenseCategory
from glas_osla.db.models.revenues_plots_md import RevenueCategory

ask_keyboard = InlineKeyboardMarkup(row_width=1)
ask_keyboard.add(InlineKeyboardButton('Доходы', callback_data=f'cd_cat_r'))
ask_keyboard.add(InlineKeyboardButton('Расходы', callback_data=f'cd_cat_e'))
ask_keyboard.add(InlineKeyboardButton('Назад', callback_data=f'get_profile'))


async def del_last_for_back(callback: str) -> str:
    return '_'.join(callback.split('_')[:-1])


async def categories_keyboard(user_id, callback: str):
    if callback.split('_')[-1] == 'r':
        categories = await get_user_categories(user_id, RevenueCategory)
    else:
        categories = await get_user_categories(user_id, ExpenseCategory)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('Между категориями', callback_data=f'cd_time_{callback}_all'))
    for row in categories:
        keyboard.add(
            InlineKeyboardButton(text=row[1], callback_data=f'cd_time_{callback}_{row[0]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'get_cd'))
    return keyboard


async def time_keyboard(callback: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('День', callback_data=f'cd_show_{callback}_d'))
    keyboard.add(InlineKeyboardButton('Неделя', callback_data=f'cd_show_{callback}_w'))
    keyboard.add(InlineKeyboardButton('Месяц', callback_data=f'cd_show_{callback}_m'))
    keyboard.add(
        InlineKeyboardButton('Назад', callback_data=f'cd_cat_{await del_last_for_back(callback)}'))
    return keyboard


show_keyboard = InlineKeyboardMarkup(row_width=1)
show_keyboard.add(InlineKeyboardButton('Закрыть', callback_data='cd_close'))
