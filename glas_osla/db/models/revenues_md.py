from datetime import datetime

import sqlalchemy
from glas_osla.db.base import Base
from sqlalchemy import orm


class Revenue(Base):
    __tablename__ = "revenues"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False,
                           autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('revenues_categories.id'))
    sub_category = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey('revenues_subcategories.id'))
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    note = sqlalchemy.Column(sqlalchemy.String, nullable=True)
