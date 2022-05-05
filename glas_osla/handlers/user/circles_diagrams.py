import os
from datetime import timedelta, datetime

from aiogram.dispatcher import Dispatcher, filters
from aiogram import types
from aiogram.types import InputFile

from glas_osla.db.models.expenses_md import Expense
from glas_osla.db.models.expenses_plots_md import ExpenseSubCategory
from glas_osla.db.models.revenues_md import Revenue
from glas_osla.db.models.revenues_plots_md import RevenueSubCategory

from glas_osla.db.db_commands import (
    get_user_posts_in_time, get_category_name, get_sub_category_name,
    get_user_posts_in_time,
    get_category_name, get_category_name, get_sub_category_name,
    get_sub_category_name, get_user_subcategories, get_sub_category_amount_in_time
)
from glas_osla.utils.cirlces_diagrams import draw_circle_diagram, sum_same_categories, form_data

from glas_osla.templates.circles_diagrams_phrases import *
from glas_osla.keyboards.inline.circles_diagrams_keyboards import *


async def get_callback_data(callback: types.CallbackQuery):
    return callback.data.split('_')[-1]


async def send_callback_data(callback: types.CallbackQuery):
    return '_'.join(callback.data.split('_')[2:])


async def get_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text(choose_data_type, reply_markup=ask_keyboard)


async def get_category_for_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text(choose_data_type,
                                     reply_markup=await categories_keyboard(callback.from_user.id,
                                                                            await send_callback_data(
                                                                                callback)))


async def get_time_for_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text(choose_time, reply_markup=await time_keyboard(
        await send_callback_data(callback)))


async def show_circle_diagram(callback: types.CallbackQuery):
    data_type, category, time = callback.data.split('_')[2:]
    times = {'d': 1, 'w': 7, 'm': 30}
    time = timedelta(days=times[time])

    data = None
    if data_type == 'r':
        if category == 'all':
            data = [[i[0]] + [await get_category_name(i[1], RevenueCategory)] for i in
                    await get_user_posts_in_time(callback.from_user.id, time, Revenue)]
        else:
            data = await get_user_subcategories(callback.from_user.id, int(category),
                                                RevenueSubCategory)
            data = [[await get_sub_category_amount_in_time(callback.from_user.id, i[0], time,
                                                           Revenue)] + [i[1]] for i in data]
            data = await form_data(data)
    elif data_type == 'e':
        if category == 'all':
            data = [[i[0]] + [await get_category_name(i[1], ExpenseCategory)] for i in
                    await get_user_posts_in_time(callback.from_user.id, time, Expense)]
        else:
            data = await get_user_subcategories(callback.from_user.id, int(category),
                                                ExpenseSubCategory)
            data = [[await get_sub_category_amount_in_time(callback.from_user.id, i[0], time,
                                                           Expense)] + [i[1]] for i in data]
            data = await form_data(data)
    if not data:
        await callback.message.answer(no_data_text)
        return

    filename = f'glas_osla/resources/img/circles_diagrams/{callback.from_user.id}_{data_type}_{category}_{int(datetime.now().microsecond)}.png'

    data = await sum_same_categories(data)
    await draw_circle_diagram(filename, (i[0] for i in data), (i[1] for i in data))
    photo = InputFile(filename)
    await callback.bot.send_photo(callback.from_user.id, photo=photo, caption=your_diagram,
                                  reply_markup=show_keyboard)
    os.remove(filename)


async def close_circle_diagram(callback: types.CallbackQuery):
    await callback.message.delete()


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
    dp.register_callback_query_handler(close_circle_diagram, is_client=True, text='cd_close')
