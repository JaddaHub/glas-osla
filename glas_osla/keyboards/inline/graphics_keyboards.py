from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from glas_osla.db.db_commands import get_user_categories
from glas_osla.db.models.expenses_plots_md import ExpenseCategory
from glas_osla.db.models.revenues_plots_md import RevenueCategory

main_keyboard = InlineKeyboardMarkup(row_width=1)
main_keyboard.add(InlineKeyboardButton('Доходы', callback_data='get_r_g'))
main_keyboard.add(InlineKeyboardButton('Расходы', callback_data='get_e_g'))


async def revenues_categories_keyboard(user_id):
    categories = get_user_categories(user_id, RevenueCategory)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for row in categories:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f'rg_{row[0]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'rg_to_g'))
    return keyboard


async def expenses_categories_keyboard(user_id):
    categories = get_user_categories(user_id, ExpenseCategory)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for row in categories:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f'eg_{row[0]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'eg_to_g'))
    return keyboard


r_graphics_keyboard = InlineKeyboardMarkup(row_width=1)
r_graphics_keyboard.add(InlineKeyboardButton('Неделя', callback_data='show_r_w_g'))
r_graphics_keyboard.add(InlineKeyboardButton('Месяц', callback_data='show_r_m_g'))
r_graphics_keyboard.add(InlineKeyboardButton('Год', callback_data='show_r_y_g'))
r_graphics_keyboard.add(InlineKeyboardButton('Назад', callback_data='get_profile'))

e_graphics_keyboard = InlineKeyboardMarkup(row_width=1)
e_graphics_keyboard.add(InlineKeyboardButton('Неделя', callback_data='show_e_w_g'))
e_graphics_keyboard.add(InlineKeyboardButton('Месяц', callback_data='show_e_m_g'))
e_graphics_keyboard.add(InlineKeyboardButton('Год', callback_data='show_e_y_g'))
e_graphics_keyboard.add(InlineKeyboardButton('Назад', callback_data='get_profile'))
