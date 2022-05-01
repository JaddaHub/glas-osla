from aiogram.dispatcher import Dispatcher
from aiogram import types
from glas_osla.db.base import get_session
from glas_osla.db.users import User
from sqlalchemy import select


async def profile(message: types.Message):
    async with get_session() as db_sess:
        data = await db_sess.execute(select(User))
    await message.answer(data.all())


def setup_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(profile, commands='profile', is_client=True)
