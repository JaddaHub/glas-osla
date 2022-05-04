from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from glas_osla.db import db_commands
from glas_osla.db.models.revenues_plots_md import RevenueCategory, RevenueSubCategory


async def revenues_categories_keyboard(message_author_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    response = await db_commands.get_user_categories(message_author_id, RevenueCategory)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"r_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='Добавить категорию', callback_data='add_r_c'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='r_c_back_to_menu'))
    return keyboard


async def revenues_subcategories_keyboard(message_author_id, category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    response = await db_commands.get_user_subcategories(message_author_id, category_id, RevenueSubCategory)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"r_s_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='Редактировать категорию', callback_data=f'change_r_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='Добавить подкатегорию', callback_data=f'add_r_s_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_r_categories'))
    return keyboard


async def change_or_delete_revenues_category(category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Изменить', callback_data=f'edit_r_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data=f'del_r_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'back_to_r_categories'))
    return keyboard


async def change_or_delete_revenues_sub_category(sub_category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Изменить', callback_data=f'edit_r_s_c_{sub_category_id}'))
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data=f'del_r_s_c_{sub_category_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'back_to_r_c_{sub_category_id}'))
    return keyboard


async def edit_revenues_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно', callback_data=f'edit_back_to_r_categories'))
    return keyboard


async def edit_revenues_sub_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно', callback_data=f'edit_back_to_r_categories'))
    return keyboard
