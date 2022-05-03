from aiogram.dispatcher import Dispatcher
from aiogram import types

from glas_osla.db.base import async_session
from glas_osla.db import db_commands
from glas_osla.db.models.users_md import User
from glas_osla.filters.is_client import ClientFilter
from glas_osla.templates import general_phrases
from glas_osla.keyboards.inline import keyboards
from sqlalchemy import select

from glas_osla.handlers.user.circles_diagrams import setup_circles_diagrams_handlers
from glas_osla.handlers.user.graphics import setup_graphics_handlers
from glas_osla.handlers.user.reports import setup_reports_handlers


async def profile(callback: types.CallbackQuery):
    async with async_session() as db_sess:
        query = select(User.tg_id, User.name, User.person_type, User.created_date).where(
            User.tg_id == callback.from_user.id)
        data = map(str, (await db_sess.execute(query)).first())
    await callback.message.answer(f"Информация о вас:\n{' '.join(data)}",
                                  reply_markup=keyboards.profile_keyboard)


async def show_menu(message: types.Message):
    user_nickname = await db_commands.get_user_nickname(message.from_user.id)
    await message.answer(general_phrases.menu_text.format(user_nickname),
                         reply_markup=keyboards.menu_keyboard)


async def show_quick_info(message: types.Message):
    await message.answer(general_phrases.quick_info_text, reply_markup=keyboards.menu_keyboard)


async def show_expenses_categories(callback: types.CallbackQuery):
    expenses_keyboard = await keyboards.expenses_categories_keyboard(callback.from_user.id)
    await callback.message.answer("Ваши категории у расходов", reply_markup=expenses_keyboard)


async def show_revenues_categories(callback: types.CallbackQuery):
    revenues_keyboard = await keyboards.revenues_categories_keyboard(callback.from_user.id)
    await callback.message.answer('Ваши категории у доходов', reply_markup=revenues_keyboard)


async def profile_back_to_menu(callback: types.CallbackQuery):
    user_nickname = await db_commands.get_user_nickname(callback.from_user.id)
    await callback.message.answer(general_phrases.menu_text.format(user_nickname),
                                  reply_markup=keyboards.menu_keyboard)


async def add_expenses_category(message: types.Message):
    cat_name = message.text.split()[1]
    await db_commands.add_expenses_category(message.from_user.id, cat_name)
    await message.answer('OK, категория добавлена', reply_markup=keyboards.menu_keyboard)


async def add_expenses_sub_category(message: types.Message):
    sub_cat_name, parent_name = message.text.split()[1:3]
    parent_id = await db_commands.get_expenses_category_id(parent_name)
    await db_commands.add_expenses_sub_category(message.from_user.id, parent_id, sub_cat_name)
    await message.answer('OK, подкатегория добавлена', reply_markup=keyboards.menu_keyboard)


def setup_general_handlers(dp: Dispatcher):
    dp.register_message_handler(show_menu, ClientFilter(True), commands='menu')
    dp.register_message_handler(show_quick_info, ClientFilter(True), commands='quick')
    dp.register_callback_query_handler(profile, ClientFilter(True), text='get_profile')
    dp.register_callback_query_handler(show_expenses_categories, text='get_expenses')
    dp.register_callback_query_handler(show_revenues_categories, text='get_revenues')
    dp.register_callback_query_handler(profile_back_to_menu, text='profile_back_to_menu')
    setup_circles_diagrams_handlers(dp)
    setup_graphics_handlers(dp)
    setup_reports_handlers(dp)
    dp.register_callback_query_handler(show_expenses_categories, ClientFilter(True),
                                       text='get_expenses')
    dp.register_callback_query_handler(show_revenues_categories, ClientFilter(True),
                                       text='get_revenues')

    dp.register_message_handler(add_expenses_category, ClientFilter(True), commands='newcat')
    dp.register_message_handler(add_expenses_sub_category, ClientFilter(True), commands='newsubcat')
