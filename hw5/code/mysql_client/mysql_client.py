import pymysql
from pymysql.cursors import DictCursor

from names import LOGS_TABLE, ID_F, LOCATION_F, METHOD_F, IP_F
from names import STATUS_CODE_F, RESPONSE_SIZE_F, DATETIME_F
from utils import LogsRecord, InvalidIdException


class MysqlClient:

    def __init__(self, user, password, db_name, port: int = 3306):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = '127.0.0.1'
        self.port = port
        self.charset = 'utf8'

        self.connection = self.connect()

    def get_connection(self, db_created=False):
        return pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                               db=self.db_name if db_created else None,
                               charset=self.charset, cursorclass=DictCursor, autocommit=True)

    def connect(self):
        connection = self.get_connection()

        connection.query(f'DROP DATABASE IF EXISTS {self.db_name}')
        connection.query(f'CREATE DATABASE {self.db_name}')

        connection.close()

        return self.get_connection(db_created=True)

    def insert(self, query) -> int:
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.lastrowid

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def create_nginx_logs(self):
        query = f"""
           CREATE TABLE IF NOT EXISTS `{LOGS_TABLE}` (
             `{ID_F}` INT NOT NULL AUTO_INCREMENT,
             `{IP_F}` CHAR(15) NOT NULL,
             `{METHOD_F}` CHAR(10) NOT NULL,
             `{LOCATION_F}` TEXT NOT NULL,
             `{STATUS_CODE_F}` INT NOT NULL,
             `{RESPONSE_SIZE_F}` INT NOT NULL,
             `{DATETIME_F}` DATETIME NOT NULL DEFAULT '2020-01-01',
             PRIMARY KEY (`{ID_F}`)
           ) CHARSET=utf8
           """
        self.execute_query(query)

    def add_record(self, record: LogsRecord) -> int:
        ip = record.ip
        method = record.method
        location = record.location
        status_code = record.status_code
        response_size = record.response_size
        datetime = record.time
        query = (f"INSERT INTO {LOGS_TABLE} "
                 f"({IP_F}, {METHOD_F}, {LOCATION_F}, {STATUS_CODE_F}, {RESPONSE_SIZE_F}, {DATETIME_F}) "
                 "VALUES "
                 f"('{ip}', '{method}', '{location}', {status_code}, {response_size}, '{datetime}')")
        return self.insert(query)

    def get_record(self, record_id: int) -> LogsRecord:
        result = self.execute_query(f"SELECT * FROM {LOGS_TABLE} WHERE {ID_F}={record_id}")
        if len(result) == 0:
            raise InvalidIdException
        result = result[0]
        return LogsRecord(ip=result[IP_F],
                          method=result[METHOD_F],
                          location=result[LOCATION_F],
                          status_code=result[STATUS_CODE_F],
                          response_size=result[RESPONSE_SIZE_F],
                          time=result[DATETIME_F]
                          )
