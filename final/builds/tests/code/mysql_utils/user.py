from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

from mysql_utils.record import Record
from settings import TABLENAME

Base = declarative_base()


class User(Base):
    __tablename__ = TABLENAME

    id = Column(Integer, autoincrement=True, nullable=False)
    username = Column(String(16), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(SmallInteger, nullable=True, default=None)
    active = Column(SmallInteger, nullable=True, default=None)
    start_active_time = Column(DateTime, nullable=False, default=None)
    PrimaryKeyConstraint('id')
    UniqueConstraint('username')
    UniqueConstraint('email')

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', " \
               f"password='{self.password}', access={self.access}, active={self.active}, " \
               f"start_active_time='{self.start_active_time}')>"

    def to_record(self):
        return Record(
            username=self.username,
            email=self.email,
            password=self.password,
            access=self.access,
            active=self.active,
            start_active_time=self.start_active_time.timestamp())
