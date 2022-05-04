from datetime import timedelta

from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.types import InputFile

from glas_osla.db.db_commands import get_user_in_time, get_category_name, get_sub_category_name
from glas_osla.db.models.expenses_md import Expense
from glas_osla.db.models.expenses_plots_md import ExpenseSubCategory, ExpenseCategory
from glas_osla.db.models.revenues_md import Revenue
from glas_osla.db.models.revenues_plots_md import RevenueCategory, RevenueSubCategory
from glas_osla.keyboards.inline import graphics_keyboards


async def get_graphics(callback: types.CallbackQuery):
    await callback.message.answer('Выберите о чем построить график',
                                  reply_markup=graphics_keyboards.main_keyboard)


async def get_revenues_graphics(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите отрезок на котором будет построен график',
                                     reply_markup=graphics_keyboards.r_graphics_keyboard)


async def get_expenses_graphics(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите отрезок на котором будет построен график',
                                     reply_markup=graphics_keyboards.e_graphics_keyboard)


async def show_week_graphic(callback: types.CallbackQuery):
    time = timedelta(days=7)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    expenses = await get_user_expenses_in_time(callback.from_user.id, time)

    revenues = [[i[0]] + [await get_category_name(i[1], RevenueCategory)] + [
        await get_sub_category_name(i[2], RevenueSubCategory)] for i in revenues]

    expenses = [[i[0]] + [await get_category_name(i[1], ExpenseCategory)] + [
        await get_sub_category_name(i[2], ExpenseSubCategory)] for i in expenses]

    filename_r = 'day_cd_revenues.png'
    filename_e = 'day_cd_expenses.png'
    draw_circle_diagram(filename_r, (i[1] for i in revenues), (i[0] for i in revenues))
    photo_r = InputFile(filename_r)
    draw_circle_diagram(filename_e, (i[1] for i in expenses), (i[0] for i in expenses))
    photo_e = InputFile(filename_e)

    await callback.bot.send_photo(callback.from_user.id, photo=photo_r, caption='Ваша диаграмма')
    await callback.bot.send_photo(callback.from_user.id, photo=photo_e, caption='Ваша диаграмма')


async def show_month_graphic(callback: types.CallbackQuery):
    time = timedelta(days=30)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    expenses = await get_user_expenses_in_time(callback.from_user.id, time)

    revenues = [[i[0]] + [await get_category_name(i[1], RevenueCategory)] + [
        await get_sub_category_name(i[2], RevenueSubCategory)] for i in revenues]

    expenses = [[i[0]] + [await get_category_name(i[1], ExpenseCategory)] + [
        await get_sub_category_name(i[2], ExpenseSubCategory)] for i in expenses]

    filename_r = 'day_cd_revenues.png'
    filename_e = 'day_cd_expenses.png'
    draw_circle_diagram(filename_r, (i[1] for i in revenues), (i[0] for i in revenues))
    photo_r = InputFile(filename_r)
    draw_circle_diagram(filename_e, (i[1] for i in expenses), (i[0] for i in expenses))
    photo_e = InputFile(filename_e)

    await callback.bot.send_photo(callback.from_user.id, photo=photo_r, caption='Ваша диаграмма')
    await callback.bot.send_photo(callback.from_user.id, photo=photo_e, caption='Ваша диаграмма')


async def show_year_graphic(callback: types.CallbackQuery):
    time = timedelta(days=365)
    revenues = await get_user_in_time(callback.from_user.id, time, Revenue)
    expenses = await get_user_in_time(callback.from_user.id, time, Expense)

    revenues = [[i[0]] + [await get_category_name(i[1], RevenueCategory)] + [
        await get_sub_category_name(i[2], RevenueSubCategory)] for i in revenues]

    expenses = [[i[0]] + [await get_category_name(i[1], ExpenseCategory)] + [
        await get_sub_category_name(i[2], ExpenseSubCategory)] for i in expenses]

    filename_r = 'year_g_revenues.png'
    filename_e = 'year_g_expenses.png'
    # draw_circle_diagram(filename_r, (i[1] for i in revenues), (i[0] for i in revenues))
    # photo_r = InputFile(filename_r)
    # draw_circle_diagram(filename_e, (i[1] for i in expenses), (i[0] for i in expenses))
    # photo_e = InputFile(filename_e)

    # await callback.bot.send_photo(callback.from_user.id, photo=photo_r, caption='Ваша диаграмма')
    # await callback.bot.send_photo(callback.from_user.id, photo=photo_e, caption='Ваша диаграмма')


async def current_back_to_graphics(callback: types.CallbackQuery):
    await get_graphics(callback)


def setup_graphics_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_graphics, is_client=True, text='get_g')
    dp.register_callback_query_handler(get_revenues_graphics, is_client=True, text='get_r_g')
    dp.register_callback_query_handler(get_expenses_graphics, is_client=True, text='get_e_g')
    dp.register_callback_query_handler(show_year_graphic, is_client=True, text='show_r_y_g')
    dp.register_callback_query_handler(show_week_graphic, is_client=True, text='show_w_g')
    dp.register_callback_query_handler(show_month_graphic, is_client=True, text='show_m_g')
    dp.register_callback_query_handler(current_back_to_graphics, is_client=True,
                                       text='current_back_to_g')
