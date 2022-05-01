import sqlalchemy
from glas_osla.db.base import Base
from sqlalchemy import orm


class Expense(Base):
    __tablename__ = "expenses"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('expenses_categories.id'))
    sub_category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('expenses_subcategories.id'))
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    note = sqlalchemy.Column(sqlalchemy.String, nullable=True)
