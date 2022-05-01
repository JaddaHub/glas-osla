from aiogram.dispatcher.filters import BoundFilter
from glas_osla.db.base import async_session
from glas_osla.db.models.users_md import User
from sqlalchemy import select


class ClientFilter(BoundFilter):
    key = 'is_client'

    def __init__(self, is_client):
        self.is_client = is_client

    async def check(self, obj):
        if self.is_client is None:
            return False
        async with async_session() as db_sess:
            query = select(User.tg_id)
            all_users = [i[0] for i in (await db_sess.execute(query)).all()]
            return (obj.from_user.id in set(all_users)) == self.is_client
