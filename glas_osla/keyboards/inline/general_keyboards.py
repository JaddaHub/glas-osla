from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(InlineKeyboardButton(text='Профиль', callback_data='get_profile'))
menu_keyboard.add(InlineKeyboardButton(text='Расходы', callback_data='get_expenses'))
menu_keyboard.add(InlineKeyboardButton(text='Доходы', callback_data='get_revenues'))

profile_keyboard = InlineKeyboardMarkup(row_width=1)
profile_keyboard.add(
    InlineKeyboardButton(text='Круговые диаграммы', callback_data='get_cd'))
profile_keyboard.add(InlineKeyboardButton(text='Графики', callback_data='get_graphics'))
profile_keyboard.add(InlineKeyboardButton(text='Полный отчет', callback_data='get_full_report'))
profile_keyboard.add(InlineKeyboardButton(text='Быстрый отчет', callback_data='get_quick_report'))
profile_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='profile_back_to_menu'))


menu_button_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_button_keyboard.add(KeyboardButton(text='/menu'))