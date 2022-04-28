import logging

from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from templates.registration_phrases import *
from states.RegStates import RegistrationStates
from config.config import AUTH_KEY
from filters.is_client import IsNotClient
from data.users import User
from data import db_session


async def introduction(message: types.Message):
    await message.answer(introduction_text)


async def start_registration(message: types.Message, state: FSMContext):
    await RegistrationStates.name_period.set()
    await message.answer(registration_start_text)


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer(person_type.format(message.text))
    await RegistrationStates.next()


async def get_person_type(message: types.Message, state: FSMContext):
    new_user = User()
    new_user.tg_id = message.from_user.id
    new_user.name = (await state.get_data())['client_name']
    new_user.person_type = message.text
    db_sess = db_session.create_session()
    db_sess.add(new_user)
    db_sess.commit()
    logging.info(f"{new_user} добавлен!")
    await message.answer(thanks)
    await state.finish()


def setup_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(introduction, commands='start')
    dp.register_message_handler(start_registration, IsNotClient(), commands='reg')
    dp.register_message_handler(get_name, state=RegistrationStates.name_period)
    dp.register_message_handler(get_person_type, state=RegistrationStates.person_type_period)
