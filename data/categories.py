import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase

jobs_to_category = sqlalchemy.Table('hazard', SqlAlchemyBase.metadata,
                                    sqlalchemy.Column('jobs', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('jobs.id')),
                                    sqlalchemy.Column('category', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('category.id'))
                                    )


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
