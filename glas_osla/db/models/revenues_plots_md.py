import sqlalchemy
from glas_osla.db.base import Base


class RevenueCategory(Base):
    __tablename__ = 'revenues_categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class RevenueSubCategory(Base):
    __tablename__ = 'revenues_subcategories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True,
                           nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    parent = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('revenues_categories.id'))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
