from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from config.config import USERS


class IsClient(BoundFilter):
    async def check(self, message: Message):
        return message.from_user.id in USERS
