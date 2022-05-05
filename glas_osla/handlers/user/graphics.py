import os
from datetime import timedelta, datetime

from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher import Dispatcher, filters

from glas_osla.db.db_commands import get_category_name, get_sub_category_name, get_user_in_time
from glas_osla.db.db_commands import get_user_posts_in_time, get_category_name, get_sub_category_name
from glas_osla.db.models.expenses_md import Expense
from glas_osla.db.models.expenses_plots_md import ExpenseSubCategory
from glas_osla.db.models.revenues_md import Revenue
from glas_osla.db.models.revenues_plots_md import RevenueSubCategory
from glas_osla.templates.graphics_phrases import *
from glas_osla.keyboards.inline.graphics_keyboards import *

from glas_osla.utils.graphics import draw_graphic


async def get_callback_data(callback: types.CallbackQuery):
    return callback.data.split('_')[-1]


async def send_callback_data(callback: types.CallbackQuery):
    return '_'.join(callback.data.split('_')[2:])


async def get_graphics(callback: types.CallbackQuery):
    await callback.message.edit_text(choose_data_type, reply_markup=ask_keyboard)


async def get_category_graphics(callback: types.CallbackQuery):
    await callback.message.edit_text(choose_data_type,
                                     reply_markup=await categories_keyboard(callback.from_user.id,
                                                                            await send_callback_data(
                                                                                callback)))


async def get_time_for_graphics(callback: types.CallbackQuery):
    await callback.message.edit_text(choose_time, reply_markup=await time_keyboard(
        await send_callback_data(callback)))


async def show_graphic(callback: types.CallbackQuery):
    data_type, category, time = callback.data.split('_')[2:]
    times = {'w': 7, 'm': 30, 'y': 365}
    time = timedelta(days=times[time])

    data = None
    if data_type == 'r':
        if category == 'all':
            data = [[i[0]] + [await get_category_name(i[1], RevenueCategory)] + [
                await get_sub_category_name(i[2], RevenueSubCategory)] for i in
                    await get_user_in_time(callback.from_user.id, time, Revenue)]
        else:
            data = await get_user_subcategories(callback.from_user.id, int(category),
                                                RevenueSubCategory)
    elif data_type == 'e':
        if category == 'all':
            data = [[i[0]] + [await get_category_name(i[1], ExpenseCategory)] + [
                await get_sub_category_name(i[2], ExpenseSubCategory)] for i in
                    await get_user_in_time(callback.from_user.id, time, Expense)]
        else:
            data = await get_user_subcategories(callback.from_user.id, int(category),
                                                ExpenseSubCategory)
    if not data:
        await callback.message.answer(no_data_text)
        return

    print(data)
    filename = f'../../glas_osla/resources/img/graphics/{callback.from_user.id}_{data_type}_{category}_{int(datetime.now().microsecond)}.png'

    await draw_graphic(filename, (i[1] for i in data), (i[0] for i in data))
    photo = InputFile(filename)
    await callback.bot.send_photo(callback.from_user.id, photo=photo, caption=your_graphic,
                                  reply_markup=show_keyboard)
    os.remove(filename)


async def close_graphic(callback: types.CallbackQuery):
    await callback.message.delete()


def setup_graphics_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_graphics, is_client=True, text='get_graphics')

    dp.register_callback_query_handler(get_category_graphics, filters.Text(startswith='g_cat_'),
                                       is_client=True)

    dp.register_callback_query_handler(get_time_for_graphics, filters.Text(startswith='g_time_'),
                                       is_client=True)

    dp.register_callback_query_handler(show_graphic, filters.Text(startswith='g_show_'),
                                       is_client=True)

    dp.register_callback_query_handler(close_graphic, is_client=True, text='g_close')
