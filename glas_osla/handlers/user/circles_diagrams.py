from datetime import timedelta

from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.types import InputFile
from glas_osla.keyboards.inline import keyboards

from glas_osla.db.db_commands import (
    get_user_revenues_in_time, get_user_expenses_in_time,
    get_revenues_category_name, get_expenses_category_name, get_revenues_sub_category_name,
    get_expenses_sub_category_name
)
from glas_osla.utils.cirlces_diagrams import draw_circle_diagram


async def get_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите о чем построить диаграмму',
                                     reply_markup=keyboards.main_circles_diagrams_keyboard)


async def get_revenues_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите отрезок на котором будет построена диаграмма',
                                     reply_markup=keyboards.r_circles_diagrams_keyboard)


async def get_expenses_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите отрезок на котором будет построена диаграмма',
                                     reply_markup=keyboards.e_circles_diagrams_keyboard)


async def show_day_circle_diagram(callback: types.CallbackQuery):
    # diagram_keyboard = keyboards.current_circles_diagrams_keyboard
    time = timedelta(days=1)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    expenses = await get_user_expenses_in_time(callback.from_user.id, time)

    revenues = [[i[0]] + [await get_revenues_category_name(i[1])] + [
        await get_revenues_sub_category_name(i[2])] for i in revenues]

    expenses = [[i[0]] + [await get_expenses_category_name(i[1])] + [
        await get_expenses_sub_category_name(i[2])] for i in expenses]

    filename_r = 'day_cd_revenues.png'
    filename_e = 'day_cd_expenses.png'
    draw_circle_diagram(filename_r, (i[1] for i in revenues), (i[0] for i in revenues))
    photo_r = InputFile(filename_r)
    draw_circle_diagram(filename_e, (i[1] for i in expenses), (i[0] for i in expenses))
    photo_e = InputFile(filename_e)

    await callback.bot.send_photo(callback.from_user.id, photo=photo_r, caption='Ваша диаграмма')
    await callback.bot.send_photo(callback.from_user.id, photo=photo_e, caption='Ваша диаграмма')


async def show_week_circle_diagram(callback: types.CallbackQuery):
    # diagram_keyboard = keyboards.current_circles_diagrams_keyboard
    # photo = InputFile('glas_osla/resources/img/circles_diagrams/')
    time = timedelta(days=7)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    await callback.message.answer(f'{revenues}')
    # await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=diagram_keyboard)


async def show_month_circle_diagram(callback: types.CallbackQuery):
    # diagram_keyboard = keyboards.current_circles_diagrams_keyboard
    # photo = InputFile('glas_osla/resources/img/circles_diagrams/')
    time = timedelta(days=30)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    await callback.message.answer(f'{revenues}')
    # await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=diagram_keyboard)


async def current_back_to_circles_diagram(callback: types.CallbackQuery):
    await get_circles_diagrams(callback)


def setup_circles_diagrams_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_circles_diagrams, is_client=True, text='get_cd')
    dp.register_callback_query_handler(get_revenues_circles_diagrams, is_client=True,
                                       text='get_r_cd')
    dp.register_callback_query_handler(get_expenses_circles_diagrams, is_client=True,
                                       text='get_e_cd')

    dp.register_callback_query_handler(show_day_circle_diagram, is_client=True,
                                       text='show_r_d_cd')
    dp.register_callback_query_handler(show_week_circle_diagram, is_client=True,
                                       text='show_week_circle_diagram')
    dp.register_callback_query_handler(show_month_circle_diagram, is_client=True,
                                       text='show_month_circle_diagram')
    dp.register_callback_query_handler(current_back_to_circles_diagram, is_client=True,
                                       text='current_back_to_circles_diagrams')
