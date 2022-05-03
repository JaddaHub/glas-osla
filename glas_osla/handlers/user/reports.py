from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.types import InputFile

from glas_osla.keyboards.inline import keyboards


async def get_reports(callback: types.CallbackQuery):
    await callback.message.answer('Выберите на каком отрезке будет строиться отчёт',
                                  reply_markup=keyboards.reports_keyboard)


async def show_week_report(callback: types.CallbackQuery):
    photo = InputFile('glas_osla/resources/img/report/')
    await callback.bot.send_photo(callback.from_user.id, photo=photo,
                                  reply_markup=keyboards.current_report_keyboard)


async def show_month_report(callback: types.CallbackQuery):
    photo = InputFile('glas_osla/resources/img/report/')
    await callback.bot.send_photo(callback.from_user.id, photo,
                                  reply_markup=keyboards.current_report_keyboard)


async def show_year_report(callback: types.CallbackQuery):
    photo = InputFile('glas_osla/resources/img/report/')
    await callback.bot.send_photo(callback.from_user.id, photo,
                                  reply_markup=keyboards.current_report_keyboard)


async def current_back_to_reports(callback: types.CallbackQuery):
    await get_reports(callback)


def setup_reports_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_reports, is_client=True, text='get_reports')
    dp.register_callback_query_handler(show_week_report, is_client=True, text='show_week_report')
    dp.register_callback_query_handler(show_month_report, is_client=True, text='show_month_report')
    dp.register_callback_query_handler(show_year_report, is_client=True, text='show_year_report')
    dp.register_callback_query_handler(current_back_to_reports, is_client=True,
                                       text='current_back_to_reports')
