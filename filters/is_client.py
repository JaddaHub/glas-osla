from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data import db_session
from data.users import User


class IsClient(BoundFilter):
    async def check(self, message: Message):
        db_sess = db_session.create_session()
        return message.from_user.id in set([user.tg_id for user in db_sess.query(User).all()])


class IsNotClient(BoundFilter):
    async def check(self, message: Message):
        db_sess = db_session.create_session()
        return message.from_user.id not in set([user.tg_id for user in db_sess.query(User).all()])
