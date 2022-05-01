import logging

from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram import types
from glas_osla.templates.registration_phrases import *
from glas_osla.states.RegStates import RegistrationStates
from glas_osla.db.users import User
from glas_osla.db.base import get_session


async def warn_to_reg(message: types.Message):
    await message.answer(need_to_reg.format(message.from_user.username))


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
    async with get_session() as db_sess:
        db_sess.add(new_user)
        db_sess.commit()
    logging.info(f"{new_user} добавлен!")
    await message.answer(thanks)
    await state.finish()


def setup_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(introduction, commands='start')
    dp.register_message_handler(start_registration, is_client=False, commands='reg')
    dp.register_message_handler(warn_to_reg, is_client=False)
    dp.register_message_handler(get_name, state=RegistrationStates.name_period)
    dp.register_message_handler(get_person_type, state=RegistrationStates.person_type_period)
