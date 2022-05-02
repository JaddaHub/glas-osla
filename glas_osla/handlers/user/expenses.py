import textwrap
from typing import Union

from aiogram.dispatcher import Dispatcher
from aiogram import types
from glas_osla.filters.is_client import ClientFilter


async def add_to_history(message: types.Message):
    arguments = message.text.split()[1:]
    if not arguments:
        await message.answer('Введите аргументы!')
        await message.delete()
        return

    await message.answer(" ".join(arguments))


def setup_expenses_handlers(dp: Dispatcher):
    dp.register_message_handler(add_to_history, ClientFilter(True), commands='-')
