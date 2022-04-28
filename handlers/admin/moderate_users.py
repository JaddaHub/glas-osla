import logging

from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from templates.registration_phrases import *
from states.RegStates import RegistrationStates
from config.config import AUTH_KEY
from filters.is_admin import IsAdmin
from data.users import User
from data import db_session


async def delete_user_from_db(message: types.Message):
    print(message)
    await message.reply('ok')


def setup_admin_moderation_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_user_from_db, IsAdmin(), commands='del')
