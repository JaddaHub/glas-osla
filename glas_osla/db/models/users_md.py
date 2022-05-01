from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from glas_osla.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    person_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    expenses = orm.relationship("Expense", backref='user')

    def __repr__(self):
        return f"<USER> {self.id} {self.name} {self.person_type}"


class BlackListUser(Base):
    __tablename__ = 'black_list'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    reason = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ban_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
