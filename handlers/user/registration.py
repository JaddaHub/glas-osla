from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from templates.registration_phrases import *
from states.RegStates import RegistrationStates
from config.config import AUTH_KEY
from filters.is_client import IsClient


async def introduction(message: types.Message):
    await message.answer(introduction_text)


async def start_registration(message: types.Message):
    await RegistrationStates.start.set()
    await message.answer(registration_start_text)


async def get_auth_key(message: types.Message, state: FSMContext):
    if message.text != AUTH_KEY:
        await message.answer(invalid_key_text)
        await state.finish()
        return
    await message.answer(valid_key_text)
    await state.finish()


async def get_profile(message: types.Message):
    await message.answer('profile')


def setup_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(introduction, commands='start')
    dp.register_message_handler(start_registration, commands='reg')
    dp.register_message_handler(get_auth_key, state=RegistrationStates.start)
    dp.register_message_handler(get_profile, IsClient(), commands='profile')
