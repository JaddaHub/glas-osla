import datetime

from aiogram import types, filters
from aiogram.dispatcher import Dispatcher, FSMContext
from glas_osla.templates.general_phrases import *
from glas_osla.db import db_commands
from glas_osla.db.models.expenses_md import Expense
from glas_osla.db.models.revenues_md import Revenue
from glas_osla.db.models.revenues_plots_md import RevenueCategory, RevenueSubCategory
from glas_osla.db.models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from glas_osla.filters.is_client import ClientFilter
from glas_osla.keyboards.inline import stat_keyboards, general_keyboards
from glas_osla.utils.analyse_data import make_deduction
from glas_osla.states.ReportStates import EnterDateStates


async def get_full_stat_type(callback: types.CallbackQuery):
    keyboard = await stat_keyboards.choose_full_stat_type_keyboard()
    await callback.message.edit_text(revenues_or_expenses_text, reply_markup=keyboard)


async def get_full_stat_period(callback: types.CallbackQuery):
    stat_type = callback.data.split("_")[-1]
    keyboard = await stat_keyboards.choose_full_period_keyboard(stat_type)
    await callback.message.edit_text(full_report_text, reply_markup=keyboard)


async def special_date(callback: types.CallbackQuery, state: FSMContext):
    db_model = callback.data.split('_')[-1]
    if db_model == 'e':
        db_model = Expense
    else:
        db_model = Revenue
    await callback.message.edit_text(enter_new_date)
    await EnterDateStates.new_date.set()
    await state.update_data(db_model=db_model)


async def get_special_date(message: types.Message, state: FSMContext):
    help_dict = {
        Revenue: (RevenueCategory, RevenueSubCategory),
        Expense: (ExpenseCategory, ExpenseSubCategory)
    }

    db_model = (await state.get_data())['db_model']
    period = message.text.replace(" ", '')
    if period == "all":
        user_data = await db_commands.all_user_posts(message.from_user.id, db_model)
    elif len(period.split('-')) != 2:
        keyboard = await stat_keyboards.back_to_profile_keyboard()
        await message.edit_text(wrong_date_input, reply_markup=keyboard)
        return
    elif period.split("-")[-1] == 'now':
        first_date = period.split("-")[0]
        day, month, year = map(int, first_date.split('.'))
        date_before = datetime.date(day=day, month=month, year=year)
        date_now = datetime.date.today()
        delta = datetime.timedelta((date_now - date_before).days)
        user_data = await db_commands.get_user_posts_in_time(message.from_user.id, delta, db_model)
    elif period.split('-')[-1] == 'one':
        first_date = period.split("-")[0]
        day, month, year = map(int, first_date.split('.'))
        curr_date = datetime.date(day=day, month=month, year=year)
        user_data = await db_commands.get_user_current_day_post(message.from_user.id, curr_date, db_model)
    else:
        first_date, second_date = period.split("-")[0], period.split("-")[1]
        first_day, first_month, first_year = map(int, first_date.split('.'))
        second_day, second_month, second_year = map(int, second_date.split('.'))
        date_before = datetime.date(day=first_day, month=first_month, year=first_year)
        date_after = datetime.date(day=second_day, month=second_month, year=second_year)
        user_data = await db_commands.get_user_current_segment_posts(message.from_user.id, date_before, date_after,
                                                                     db_model)
    another_models = help_dict[db_model]
    reply = '\n'.join([
        f'{post[0]} {post[1]} {await db_commands.get_category_name(post[2], another_models[0])} {await db_commands.get_sub_category_name(post[3], another_models[1])}'
        for post in user_data])
    if len(reply) == 0:
        reply = 'Нет данных'
    keyboard = await stat_keyboards.back_to_profile_keyboard()
    await state.finish()
    await message.answer(reply, reply_markup=keyboard)


async def get_full_statistic(callback: types.CallbackQuery):
    help_dict = {
        Revenue: (RevenueCategory, RevenueSubCategory),
        Expense: (ExpenseCategory, ExpenseSubCategory)
    }
    period, stat_type = callback.data.split("_")[3:5]
    if period == 'd':
        first_day = datetime.date.today()
    elif period == 'w':
        first_day = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
    elif period == 'm':
        first_day = datetime.date(day=1, month=datetime.date.today().month, year=datetime.date.today().year)
    if stat_type == 'e':
        db_model = Expense
    elif stat_type == 'r':
        db_model = Revenue

    another_models = help_dict[db_model]
    user_data = await db_commands.get_user_current_segment_posts(callback.from_user.id, first_day,
                                                                 datetime.date.today() + datetime.timedelta(days=1),
                                                                 db_model)
    reply = ""
    for post in user_data:
        print(post[2], post[3])
        reply += f'{post[0]} {post[1]} {await db_commands.get_category_name(post[2], another_models[0])} {await db_commands.get_sub_category_name(post[3], another_models[1])}\n'
    keyboard = await stat_keyboards.back_to_profile_keyboard()
    if len(reply) == 0:
        reply = 'Нет данных'
    await callback.message.edit_text(reply, reply_markup=keyboard)


async def get_quick_stat_type(callback: types.CallbackQuery):
    keyboard = await stat_keyboards.choose_quick_stat_type_keyboard()
    await callback.message.edit_text(revenues_or_expenses_text, reply_markup=keyboard)


async def get_quick_stat_period(callback: types.CallbackQuery):
    stat_type = callback.data.split("_")[-1]
    keyboard = await stat_keyboards.choose_quick_period_keyboard(stat_type)
    await callback.message.edit_text(full_report_text, reply_markup=keyboard)


async def get_quick_statistic(callback: types.CallbackQuery):
    period, stat_type = callback.data.split("_")[3:5]
    if period == 'd':
        delta = datetime.timedelta(days=1)
    elif period == 'w':
        delta = datetime.timedelta(days=datetime.date.today().weekday())
    elif period == 'm':
        delta = datetime.timedelta(days=datetime.date.today().day)
    if stat_type == 'e':
        db_model = Expense
    elif stat_type == 'r':
        db_model = Revenue
    user_data = await db_commands.get_user_posts_in_time(callback.from_user.id, delta, db_model)
    deduce = await make_deduction(user_data, stat_type)
    keyboard = await stat_keyboards.back_to_profile_keyboard()
    await callback.message.edit_text(deduce, reply_markup=keyboard)


async def return_to_profile(callback: types.CallbackQuery):
    await callback.message.edit_text(your_profile_text, reply_markup=general_keyboards.profile_keyboard)


def setup_reports_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_quick_stat_type, ClientFilter(True), text='get_quick_report')
    dp.register_callback_query_handler(get_quick_stat_period, ClientFilter(True),
                                       filters.Text(startswith='choose_quick_stat_'))
    dp.register_callback_query_handler(get_quick_statistic, ClientFilter(True),
                                       filters.Text(startswith='get_quick_stat_'))
    dp.register_callback_query_handler(return_to_profile, ClientFilter(True), text='back_to_profile')
    dp.register_callback_query_handler(get_full_stat_type, ClientFilter(True), text='get_full_report')
    dp.register_callback_query_handler(get_full_stat_period, ClientFilter(True),
                                       filters.Text(startswith='choose_full_stat_'))
    dp.register_callback_query_handler(special_date, ClientFilter(True), filters.Text(startswith='get_full_stat_o_'))
    dp.register_message_handler(get_special_date, ClientFilter(True), state=EnterDateStates.new_date)
    dp.register_callback_query_handler(get_full_statistic, ClientFilter(True),
                                       filters.Text(startswith='get_full_stat_'))
