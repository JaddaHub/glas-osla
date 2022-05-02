from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from glas_osla.db.db_commands import get_user_expenses_categories, get_user_revenues_categories

menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(InlineKeyboardButton(text='Профиль', callback_data='get_profile'))
menu_keyboard.add(InlineKeyboardButton(text='Траты', callback_data='get_expenses'))
menu_keyboard.add(InlineKeyboardButton(text='Доходы', callback_data='get_revenues'))

profile_keyboard = InlineKeyboardMarkup(row_width=1)
profile_keyboard.add(
    InlineKeyboardButton(text='Круговые диаграммы', callback_data='get_circles_diagrams'))
profile_keyboard.add(InlineKeyboardButton(text='Графики', callback_data='get_graphics'))
profile_keyboard.add(InlineKeyboardButton(text='Полный отчет', callback_data='get_reports'))
profile_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='profile_back_to_menu'))

circles_diagrams_keyboard = InlineKeyboardMarkup(row_width=1)
circles_diagrams_keyboard.add(InlineKeyboardButton('День', callback_data='show_day_circle_diagram'))
circles_diagrams_keyboard.add(
    InlineKeyboardButton('Неделя', callback_data='show_week_circle_diagram'))
circles_diagrams_keyboard.add(
    InlineKeyboardButton('Месяц', callback_data='show_month_circle_diagram'))
circles_diagrams_keyboard.add(
    InlineKeyboardButton('Назад', callback_data='get_profile'))

current_circles_diagrams_keyboard = InlineKeyboardMarkup(row_width=1)
current_circles_diagrams_keyboard.add(
    InlineKeyboardButton('Назад', callback_data='current_back_to_circles_diagrams'))

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


async def revenues_categories_keyboard(message_author_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    response = await get_user_revenues_categories(message_author_id)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"r_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='r_c_to_menu'))
    return keyboard
