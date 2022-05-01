import sqlalchemy
from .base import Base
from sqlalchemy import orm


class Expenses(Base):
    __tablename__ = "ExpencesData"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('UsersGeneralData.id'))
    user = orm.relationship('User')
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ExpensesCategories.id'))
    sub_category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ExpensesSubCategories.id'))
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    note = sqlalchemy.Column(sqlalchemy.String, nullable=True)
