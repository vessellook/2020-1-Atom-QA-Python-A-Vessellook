"""Module with class to connect to mysql test server"""
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from mysql_utils.user import User
from settings import Settings


class MysqlClient:
    """Class to connect to mysql test server"""

    def __init__(self, settings: Settings):  # noqa:
        """Default values will not be changed in this project"""
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}'
            f'@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}')
        self.create_session = sessionmaker(bind=self.engine)

    def get_user(self, username: str) -> Optional[User]:
        """Select user by username and return it"""
        return self.create_session().query(User).filter_by(username=username).first()

    def add_registered_user(self, username: str, email: str, password: str):
        """Insert user that was registered"""
        session = self.create_session()
        session.add(User(username=username, email=email, password=password,
                         access=1, active=0))
        session.commit()

    def clean(self):
        """Delete all records from table with users

        You need to call `insert_admin()` after it"""
        session = self.create_session()
        for user in session.query(User).all():
            session.delete(user)
        session.commit()
