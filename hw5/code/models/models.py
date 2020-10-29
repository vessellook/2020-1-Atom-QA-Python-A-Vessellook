from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from utils import LogsRecord
from names import LOGS_TABLE

Base = declarative_base()


class OrmLogsRecord(Base):
    __tablename__ = LOGS_TABLE
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    method = Column(String(20), nullable=False)
    location = Column(Text, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_size = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False, default='2020-01-01')

    def __repr__(self):
        return (f"<LogRecord("
                f"id='{self.id}',"
                f"method='{self.method}', "
                f"location='{self.location}', "
                f"status_code='{self.status_code}'"
                f"response_size='{self.response_size}'"
                f"time='{self.time}'"
                f")>")

    @staticmethod
    def from_logs_record(r: LogsRecord):
        return OrmLogsRecord(
            ip=r.ip,
            method=r.method,
            location=r.location,
            status_code=r.status_code,
            response_size=r.response_size,
            time=r.time
        )
