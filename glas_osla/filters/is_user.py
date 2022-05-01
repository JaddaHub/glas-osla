from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from ..db import db_session
from glas_osla.db.users import User


class IsUser(BoundFilter):
    async def check(self, message: Message):
        db_sess = db_session.create_session()
        return message.from_user.id not in set([user.tg_id for user in db_sess.query(User).all()])


class IsBlackListUser(BoundFilter):
    async def check(self, message: Message):
        db_sess = db_session.create_session()
        return message.from_user.id in set([user.tg_id for user in db_sess.query(User).all()])
