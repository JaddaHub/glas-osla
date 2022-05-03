from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from glas_osla.db.db_commands import (
    get_user_expenses_categories, get_user_revenues_categories,
    get_user_expenses_subcategories
)

main_circles_diagrams_keyboard = InlineKeyboardMarkup(row_width=1)
main_circles_diagrams_keyboard.add(InlineKeyboardButton('Доходы', callback_data='get_r_cd'))
main_circles_diagrams_keyboard.add(InlineKeyboardButton('Расходы', callback_data='get_e_cd'))


async def revenues_categories_keyboard(user_id):
    categories = get_user_revenues_categories(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for row in categories:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f'rcd_{row[0]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'rcd_to_cd'))
    return keyboard


async def expenses_categories_keyboard(user_id):
    categories = get_user_expenses_categories(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for row in categories:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f'rcd_{row[0]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'rcd_to_cd'))
    return keyboard


r_circles_diagrams_keyboard = InlineKeyboardMarkup(row_width=1)
r_circles_diagrams_keyboard.add(InlineKeyboardButton('День', callback_data='show_r_d_cd'))
r_circles_diagrams_keyboard.add(InlineKeyboardButton('Неделя', callback_data='show_r_w_cd'))
r_circles_diagrams_keyboard.add(InlineKeyboardButton('Месяц', callback_data='show_r_m_cd'))
r_circles_diagrams_keyboard.add(InlineKeyboardButton('Назад', callback_data='get_profile'))

e_circles_diagrams_keyboard = InlineKeyboardMarkup(row_width=1)
e_circles_diagrams_keyboard.add(InlineKeyboardButton('День', callback_data='show_e_d_cd'))
e_circles_diagrams_keyboard.add(InlineKeyboardButton('Неделя', callback_data='show_e_w_cd'))
e_circles_diagrams_keyboard.add(InlineKeyboardButton('Месяц', callback_data='show_e_m_cd'))
e_circles_diagrams_keyboard.add(InlineKeyboardButton('Назад', callback_data='get_profile'))