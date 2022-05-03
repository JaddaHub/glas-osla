from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
    KeyboardButton, Message
)
from aiogram.utils.callback_data import CallbackData

from glas_osla.db.db_commands import (
    get_user_expenses_categories, get_user_revenues_categories,
    get_user_expenses_subcategories
)

from .circles_diagrams_keyboards import (
    main_circles_diagrams_keyboard, r_circles_diagrams_keyboard,
    e_circles_diagrams_keyboard
)

board_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
board_menu_keyboard.add(KeyboardButton('/menu'))

menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(InlineKeyboardButton(text='Профиль', callback_data='get_profile'))
menu_keyboard.add(InlineKeyboardButton(text='Расходы', callback_data='get_expenses'))
menu_keyboard.add(InlineKeyboardButton(text='Доходы', callback_data='get_revenues'))

profile_keyboard = InlineKeyboardMarkup(row_width=1)
profile_keyboard.add(
    InlineKeyboardButton(text='Круговые диаграммы', callback_data='get_cd'))
profile_keyboard.add(InlineKeyboardButton(text='Графики', callback_data='get_graphics'))
profile_keyboard.add(InlineKeyboardButton(text='Полный отчет', callback_data='get_reports'))
profile_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='profile_back_to_menu'))

graphics_keyboard = InlineKeyboardMarkup(row_width=1)
graphics_keyboard.add(InlineKeyboardButton('Неделя', callback_data='show_week_graphic'))
graphics_keyboard.add(InlineKeyboardButton('Месяц', callback_data='show_month_graphic'))
graphics_keyboard.add(InlineKeyboardButton('Год', callback_data='show_year_graphic'))
graphics_keyboard.add(InlineKeyboardButton('Назад', callback_data='get_profile'))

current_graphic_keyboard = InlineKeyboardMarkup(row_width=1)
current_graphic_keyboard.add(
    InlineKeyboardButton('Назад', callback_data='current_back_to_graphics'))

reports_keyboard = InlineKeyboardMarkup(row_width=1)
reports_keyboard.add(InlineKeyboardButton('Неделя', callback_data='show_week_report'))
reports_keyboard.add(InlineKeyboardButton('Месяц', callback_data='show_month_report'))
reports_keyboard.add(InlineKeyboardButton('Год', callback_data='show_year_report'))
reports_keyboard.add(InlineKeyboardButton('Назад', callback_data='get_profile'))

current_report_keyboard = InlineKeyboardMarkup(row_width=1)
current_report_keyboard.add(InlineKeyboardButton('Назад', callback_data='current_back_to_reports'))


async def expenses_categories_keyboard(message_author_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    response = await get_user_expenses_categories(message_author_id)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"e_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='e_c_back_to_menu'))
    return keyboard


async def expenses_subcategories_keyboard(message_author_id, category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Изменить/удалить', callback_data=f'change_e_c_{category_id}'))
    response = await get_user_expenses_subcategories(message_author_id, category_id)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"e_s_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_categories'))
    return keyboard


async def change_or_delete_expenses_category(category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Изменить', callback_data=f'edit_e_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data=f'del_e_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'back_to_categories'))
    return keyboard


async def change_or_delete_expenses_sub_category(sub_category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Изменить', callback_data=f'edit_e_s_c_{sub_category_id}'))
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data=f'del_e_s_c_{sub_category_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'back_to_c_{sub_category_id}'))
    return keyboard


async def edit_expenses_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно', callback_data=f'back_to_categories'))
    return keyboard


async def edit_expenses_sub_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно', callback_data=f'back_to_categories'))
    return keyboard


async def revenues_categories_keyboard(message_author_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    response = await get_user_revenues_categories(message_author_id)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"r_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='r_c_to_menu'))
    return keyboard
