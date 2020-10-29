import sqlalchemy
from names import LOGS_TABLE, ID_F, LOCATION_F, METHOD_F, IP_F
from names import STATUS_CODE_F, RESPONSE_SIZE_F, DATETIME_F

from sqlalchemy.orm import sessionmaker

from names import ORM_QUERIES_DB
from utils import LogsRecord
from models.models import Base, OrmLogsRecord
from names import LOGS_TABLE


class MysqlOrmClient:
    def __init__(self, user, password, db_name, port: int = 3306):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port
        self.host = '127.0.0.1'
        self.connection = self.connect()
        self.engine = self.connection.engine
        session = sessionmaker(bind=self.connection)
        self.session = session()

    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db_name if db_created else ''
        ))
        return engine.connect()

    def connect(self):
        connection = self.get_connection(db_created=False)
        connection.execute(f'DROP DATABASE IF EXISTS {ORM_QUERIES_DB}')
        connection.execute(f'CREATE DATABASE {ORM_QUERIES_DB}')
        connection.close()
        return self.get_connection(db_created=True)

    def create_nginx_logs(self) -> None:
        if not self.engine.dialect.has_table(self.engine, LOGS_TABLE):
            Base.metadata.tables[LOGS_TABLE].create(self.engine)

    def add_record(self, r: LogsRecord) -> OrmLogsRecord:
        record = OrmLogsRecord.from_logs_record(r)
        # Сохраняем объект в сессии, открытой в connection
        self.session.add(record)
        # Записываем созданную запись в базу
        self.session.commit()
        # Возвращаем объект для работы из тестов
        return record

    def delete_record(self, record: OrmLogsRecord) -> None:
        self.session.delete(record)
        self.session.commit()

    def has_record(self, record: OrmLogsRecord) -> bool:
        return self.session.query(OrmLogsRecord).get(record.id) is not None
