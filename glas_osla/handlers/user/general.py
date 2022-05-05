from aiogram.dispatcher import Dispatcher
from aiogram import types

from glas_osla.db.base import async_session
from glas_osla.db import db_commands
from glas_osla.db.models.users_md import User
from glas_osla.filters.is_client import ClientFilter
from glas_osla.templates.general_phrases import *
from glas_osla.keyboards.inline import (
    general_keyboards as keyboards,
    expenses_keyboards as ex_keyboards,
    revenues_keyboards as re_keyboards
)
from sqlalchemy import select
from glas_osla.db.models.expenses_plots_md import ExpenseCategory


# from glas_osla.handlers.user.reports import setup_reports_handlers


async def profile(callback: types.CallbackQuery):
    await callback.message.edit_text(your_profile_text, reply_markup=keyboards.profile_keyboard)


async def show_menu(message: types.Message):
    user_nickname = await db_commands.get_user_nickname(message.from_user.id)
    await message.answer(menu_text.format(user_nickname),
                         reply_markup=keyboards.menu_keyboard)


async def show_quick_info(message: types.Message):
    await message.answer(quick_info_text, reply_markup=keyboards.menu_keyboard)


async def show_expenses_categories(callback: types.CallbackQuery):
    expenses_keyboard = await ex_keyboards.expenses_categories_keyboard(callback.from_user.id)
    await callback.message.edit_text(your_expenses_cat_text, reply_markup=expenses_keyboard)


async def show_revenues_categories(callback: types.CallbackQuery):
    revenues_keyboard = await re_keyboards.revenues_categories_keyboard(callback.from_user.id)
    await callback.message.edit_text(your_revenues_cat_text, reply_markup=revenues_keyboard)


async def profile_back_to_menu(callback: types.CallbackQuery):
    user_nickname = await db_commands.get_user_nickname(callback.from_user.id)
    await callback.message.edit_text(menu_text.format(user_nickname),
                                     reply_markup=keyboards.menu_keyboard)


def setup_general_handlers(dp: Dispatcher):
    dp.register_message_handler(show_menu, ClientFilter(True), commands='menu')
    dp.register_message_handler(show_quick_info, ClientFilter(True), commands='quick')
    dp.register_callback_query_handler(profile, ClientFilter(True), text='get_profile')
    dp.register_callback_query_handler(show_expenses_categories, ClientFilter(True),
                                       text='get_expenses')
    dp.register_callback_query_handler(show_revenues_categories, ClientFilter(True),
                                       text='get_revenues')
    dp.register_callback_query_handler(profile_back_to_menu, text='profile_back_to_menu')
