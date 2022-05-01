from aiogram.dispatcher import Dispatcher
from aiogram import types


async def delete_user_from_db(message: types.Message):
    await message.reply('ok')


def setup_admin_moderation_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_user_from_db, is_admin=True, commands='del')
