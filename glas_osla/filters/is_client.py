from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from glas_osla.db.base import get_session
from glas_osla.db.users import User
import typing


class ClientFilter(BoundFilter):
    key = 'is_client'

    def __init__(self, is_client: typing.Optional[bool] = None):
        self.is_client = is_client

    async def check(self, obj):
        if self.is_client is None:
            return False
        db_sess = await get_session()
        return (obj.from_user.id in set([user.tg_id for user in db_sess.query(User).all()])) == self.is_client
