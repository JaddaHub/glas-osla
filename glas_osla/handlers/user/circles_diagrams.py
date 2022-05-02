from datetime import timedelta

from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.types import InputFile
from glas_osla.keyboards.inline import keyboards

from glas_osla.db.db_commands import get_user_revenues_in_time


async def get_circles_diagrams(callback: types.CallbackQuery):
    await callback.message.answer('Выберите на каком отрезке будет строиться диаграмма',
                                  reply_markup=keyboards.circles_diagrams_keyboard)


async def show_day_circle_diagram(callback: types.CallbackQuery):
    diagram_keyboard = keyboards.current_circles_diagrams_keyboard
    # photo = InputFile('glas_osla/resources/img/circles_diagrams/')
    time = timedelta(days=1)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    await callback.message.answer(f'{revenues}', reply_markup=diagram_keyboard)
    # await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=diagram_keyboard)


async def show_week_circle_diagram(callback: types.CallbackQuery):
    diagram_keyboard = keyboards.current_circles_diagrams_keyboard
    # photo = InputFile('glas_osla/resources/img/circles_diagrams/')
    time = timedelta(days=7)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    await callback.message.answer(f'{revenues}', reply_markup=diagram_keyboard)
    # await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=diagram_keyboard)


async def show_month_circle_diagram(callback: types.CallbackQuery):
    diagram_keyboard = keyboards.current_circles_diagrams_keyboard
    # photo = InputFile('glas_osla/resources/img/circles_diagrams/')
    time = timedelta(days=30)
    revenues = await get_user_revenues_in_time(callback.from_user.id, time)
    await callback.message.answer(f'{revenues}', reply_markup=diagram_keyboard)
    # await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=diagram_keyboard)


async def current_back_to_circles_diagram(callback: types.CallbackQuery):
    await get_circles_diagrams(callback)


def setup_circles_diagrams_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_circles_diagrams, text='get_circles_diagrams')
    dp.register_callback_query_handler(show_day_circle_diagram, text='show_day_circle_diagram')
    dp.register_callback_query_handler(show_week_circle_diagram, text='show_week_circle_diagram')
    dp.register_callback_query_handler(show_month_circle_diagram, text='show_month_circle_diagram')
    dp.register_callback_query_handler(current_back_to_circles_diagram,
                                       text='current_back_to_circles_diagrams')
