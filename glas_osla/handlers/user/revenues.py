import textwrap
from typing import Union

from aiogram.dispatcher import Dispatcher
from aiogram import types
from glas_osla.filters.is_client import ClientFilter
from glas_osla.db.db_commands import quick_add_to_revenues


async def add_to_history(message: types.Message):
    try:
        arguments = message.text.split()[1:]
        if len(arguments) > 4:
            raise IndexError
    except IndexError:
        await message.answer('Введены неверные аргументы\n/quick - информация о быстрой команде')
        return

    if not arguments:
        await message.answer('Введите аргументы')
        return
    params = {
        'user_id':  message.from_user.id,
        'amount':   arguments[0],
        'category': arguments[1],
    }
    try:
        params['sub_category'] = arguments[2]
        params['note'] = arguments[3]
    except IndexError:
        pass

    await quick_add_to_revenues(params)
    await message.answer(f'запись добавлена')


def setup_revenues_handlers(dp: Dispatcher):
    dp.register_message_handler(add_to_history, ClientFilter(True), commands='+')
