from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from glas_osla.db import db_commands
from glas_osla.db.models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory


async def expenses_categories_keyboard(message_author_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    response = await db_commands.get_user_categories(message_author_id, ExpenseCategory)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"e_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='➕ Добавить категорию', callback_data='add_e_c'))
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data='e_c_back_to_menu'))
    return keyboard


async def expenses_subcategories_keyboard(message_author_id, category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    response = await db_commands.get_user_subcategories(message_author_id, category_id, ExpenseSubCategory)
    for row in response:
        keyboard.add(InlineKeyboardButton(text=row[1], callback_data=f"e_s_c_{row[0]}"))
    keyboard.add(InlineKeyboardButton(text='✏️Редактировать категорию', callback_data=f'change_e_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='➕ Добавить подкатегорию', callback_data=f'add_e_s_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_e_categories'))
    return keyboard


async def change_or_delete_expenses_category(category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='✏️Изменить', callback_data=f'edit_e_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='❌ Удалить', callback_data=f'del_e_c_{category_id}'))
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data=f'back_to_e_categories'))
    return keyboard


async def change_or_delete_expenses_sub_category(sub_category_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='✏️Изменить', callback_data=f'edit_e_s_c_{sub_category_id}'))
    keyboard.add(InlineKeyboardButton(text='❌ Удалить', callback_data=f'del_e_s_c_{sub_category_id}'))
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data=f'back_to_e_c_{sub_category_id}'))
    return keyboard


async def edit_expenses_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно 👌', callback_data=f'edit_back_to_e_categories'))
    return keyboard


async def edit_expenses_sub_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text='Понятно 👌', callback_data=f'edit_back_to_e_categories'))
    return keyboard
