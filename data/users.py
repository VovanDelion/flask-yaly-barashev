import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'martians'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String,
                                nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer,
                            nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=True)
    specialty = sqlalchemy.Column(sqlalchemy.String,
                                  nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String,
                                nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
