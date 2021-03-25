"""Module with class to connect to mysql test server"""
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from mysql_utils.record import Record
from mysql_utils.user import User
from settings import Settings


class MysqlClient:
    """Class to connect to mysql test server"""

    def __init__(self, settings: Settings):  # noqa:
        """Default values will not be changed in this project"""
        self.engine = create_engine(
            f'mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}'
            f'@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}',
            pool_recycle=3600, pool_pre_ping=True)
        self.create_session = sessionmaker(bind=self.engine)

    def get_record(self, username: str) -> Optional[Record]:
        """Select user by username and return it"""
        session = self.create_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            record = user.to_record() if user is not None else None
        except SQLAlchemyError as err:
            session.rollback()
            raise err
        else:
            session.commit()
            return record
        finally:
            session.close()

    def add_registered_user(self, username: str, email: str, password: str):
        """Insert user that was registered"""
        session = self.create_session()
        try:
            session.add(User(username=username, email=email, password=password,
                             access=1, active=0))
        except SQLAlchemyError:
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()

    def clean(self):
        """Delete all records from table with users

        You need to call `insert_admin()` after it"""
        session = self.create_session()
        try:
            session.query(User).delete()
        except SQLAlchemyError as err:
            session.rollback()
            raise err
        else:
            session.commit()
        finally:
            session.close()
