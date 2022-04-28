from handlers import *
from aiogram import Bot, Dispatcher, executor
from loader import bot, storage, dp
from data import db_session


def start():
    setup_registration_handlers(dp)
    setup_admin_moderation_handlers(dp)
    db_session.global_init()


def close():
    bot.close()
    storage.close()


if __name__ == '__main__':
    try:
        start()
        executor.start_polling(dp)
    finally:
        close()
