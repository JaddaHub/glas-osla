import logging
from handlers.user.registration import *
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config import BOT_TOKEN


def setup():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    setup_registration_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    setup()
