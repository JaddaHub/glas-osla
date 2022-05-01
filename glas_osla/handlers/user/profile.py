from aiogram.dispatcher import Dispatcher
from aiogram import types
from glas_osla.db.base import async_session
from glas_osla.db.models.users_md import User
from glas_osla.filters.is_client import ClientFilter
from sqlalchemy import select


async def profile(message: types.Message):
    async with async_session() as db_sess:
        query = select(User.tg_id, User.name, User.person_type, User.created_date).where(
            User.tg_id == message.from_user.id)
        data = map(str, (await db_sess.execute(query)).first())
    await message.answer(f"Информация о вас:\n{' '.join(data)}")


def setup_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(profile, ClientFilter(True), commands='profile')
