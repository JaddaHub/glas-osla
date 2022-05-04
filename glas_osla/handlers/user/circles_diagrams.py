import logging
import os
from datetime import timedelta

import aiogram.dispatcher.filters.state
from aiogram.dispatcher import Dispatcher, filters, FSMContext
from aiogram import types
from aiogram.types import InputFile

from glas_osla.db.models.expenses_md import Expense
from glas_osla.db.models.expenses_plots_md import ExpenseCategory, ExpenseSubCategory
from glas_osla.db.models.revenues_md import Revenue
from glas_osla.db.models.revenues_plots_md import RevenueCategory, RevenueSubCategory
from glas_osla.filters import ClientFilter
from glas_osla.keyboards.inline import general_keyboards

from glas_osla.db.db_commands import (
    get_user_in_time,
    get_category_name, get_category_name, get_sub_category_name,
    get_sub_category_name
)
from glas_osla.keyboards.inline import circles_diagrams_keyboards
from glas_osla.utils.cirlces_diagrams import draw_circle_diagram


async def get_callback_data(callback: types.CallbackQuery):
    return callback.data.split('_')[-1]


async def send_callback_data(callback: types.CallbackQuery):
    return '_'.join(callback.data.split('_')[2:])


async def get_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите о чем построить диаграмму',
                                     reply_markup=circles_diagrams_keyboards.ask_keyboard)


async def get_category_for_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите о чем построить диаграмму',
                                     reply_markup=await circles_diagrams_keyboards.categories_keyboard(
                                         callback.from_user.id,
                                         await send_callback_data(callback)))


async def get_time_for_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите отрезок времени для диаграммы',
                                     reply_markup=await circles_diagrams_keyboards.time_keyboard(
                                         await send_callback_data(callback)))


async def show_circle_diagram(callback: types.CallbackQuery):
    data_type, category, time = callback.data.split('_')[2:]
    times = {'d': 1, 'w': 7, 'm': 30}
    time = timedelta(days=times[time])

    data = None
    if data_type == 'r':
        data = [[i[0]] + [await get_category_name(i[1], RevenueCategory)] + [
            await get_sub_category_name(i[2], RevenueSubCategory)] for i in
                await get_user_in_time(callback.from_user.id, time, Revenue)]
    elif data_type == 'e':
        data = [[i[0]] + [await get_category_name(i[1], ExpenseCategory)] + [
            await get_sub_category_name(i[2], ExpenseSubCategory)] for i in
                await get_user_in_time(callback.from_user.id, time, Expense)]
    if not data:
        await callback.message.answer('Нет данных')
        return
    print(callback.data)
    print(data)

    filename = f'glas_osla/resources/img/circles_diagrams/{callback.from_user.id}_{data_type}_{category}.png'

    draw_circle_diagram(filename, (i[1] for i in data), (i[0] for i in data))
    photo = InputFile(filename)
    await callback.bot.send_photo(callback.from_user.id, photo=photo, caption='Ваша диаграмма')
    os.remove(filename)


def setup_circles_diagrams_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_circles_diagrams,
                                       is_client=True, text='get_cd')

    dp.register_callback_query_handler(get_category_for_circles_diagrams,
                                       filters.Text(startswith='cd_cat_'),
                                       is_client=True)

    dp.register_callback_query_handler(get_time_for_circles_diagrams,
                                       filters.Text(startswith='cd_time_'),
                                       is_client=True)

    dp.register_callback_query_handler(show_circle_diagram,
                                       filters.Text(startswith='cd_show_'),
                                       is_client=True)
