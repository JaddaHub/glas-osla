from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

board_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
board_menu_keyboard.add('/menu')

menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(InlineKeyboardButton(text='Профиль', callback_data='get_profile'))
menu_keyboard.add(InlineKeyboardButton(text='Расходы', callback_data='get_expenses'))
menu_keyboard.add(InlineKeyboardButton(text='Доходы', callback_data='get_revenues'))

profile_keyboard = InlineKeyboardMarkup(row_width=1)
profile_keyboard.add(
    InlineKeyboardButton(text='Круговые диаграммы', callback_data='get_cd'))
profile_keyboard.add(InlineKeyboardButton(text='Графики', callback_data='get_graphics'))
profile_keyboard.add(InlineKeyboardButton(text='Полный отчет', callback_data='get_full_report'))
profile_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='profile_back_to_menu'))
