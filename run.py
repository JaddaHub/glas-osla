import asyncio
from glas_osla.data import config
from glas_osla.db import __all_models
from glas_osla.db import base
from glas_osla.handlers import *
from glas_osla.filters import *
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

logger = logging.getLogger(__name__)


def register_all_handlers(dp):
    setup_registration_handlers(dp)
    setup_admin_moderation_handlers(dp)
    setup_expenses_handlers(dp)
    setup_revenues_handlers(dp)
    setup_general_handlers(dp)


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ClientFilter)


async def main():
    logging.basicConfig(
        format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    #await base.init_models()
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        logger.error("Bot stopped!")
