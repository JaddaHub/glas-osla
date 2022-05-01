import sqlalchemy
from .base import Base


class ExpensesCategories(Base):
    __tablename__ = 'ExpensesCategories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('UsersGeneralData.id'))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class ExpensesSubCategories(Base):
    __tablename__ = 'ExpensesSubCategories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    parent = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ExpensesCategories.id'))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
