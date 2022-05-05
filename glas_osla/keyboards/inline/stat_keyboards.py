from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def back_to_profile_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно 👌', callback_data='back_to_profile'))
    return keyboard


async def choose_quick_stat_type_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='💳 Расходы 💳', callback_data='choose_quick_stat_e'))
    keyboard.add(InlineKeyboardButton(text='💵 Доходы 💵', callback_data='choose_quick_stat_r'))
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_profile'))
    return keyboard


async def choose_quick_period_keyboard(stat_type):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='1️⃣ День', callback_data=f'get_quick_stat_d_{stat_type}'))
    keyboard.add(InlineKeyboardButton(text='7️⃣ Неделя', callback_data=f'get_quick_stat_w_{stat_type}'))
    keyboard.add(InlineKeyboardButton(text='📆 Месяц', callback_data=f'get_quick_stat_m_{stat_type}'))
    return keyboard


async def choose_full_stat_type_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='💳 Расходы 💳', callback_data='choose_full_stat_e'))
    keyboard.add(InlineKeyboardButton(text='💵 Доходы 💵', callback_data='choose_full_stat_r'))
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_profile'))
    return keyboard


async def choose_full_period_keyboard(stat_type):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='1️⃣ День', callback_data=f'get_full_stat_d_{stat_type}'))
    keyboard.add(InlineKeyboardButton(text='7️⃣ Неделя', callback_data=f'get_full_stat_w_{stat_type}'))
    keyboard.add(InlineKeyboardButton(text='📆 Месяц', callback_data=f'get_full_stat_m_{stat_type}'))
    keyboard.add(InlineKeyboardButton(text='🇲🇾 Свой вариант', callback_data=f'get_full_stat_o_{stat_type}'))
    return keyboard
