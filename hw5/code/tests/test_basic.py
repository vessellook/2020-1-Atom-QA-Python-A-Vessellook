from faker import Faker
import pytest

from utils import LogsRecord, InvalidIdException
from mysql_client.mysql_client import MysqlClient
from mysql_orm_client.mysql_orm_client import MysqlOrmClient
from names import LOGS_TABLE, ID_F


class TestMysql:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client: MysqlClient):
        self.mysql = mysql_client
        mysql_client.create_nginx_logs()

    def test_insert(self, faker: Faker):
        record = LogsRecord.fake(faker)
        record_id = self.mysql.add_record(record)
        assert record == self.mysql.get_record(record_id)
        self.mysql.execute_query(f'DELETE FROM {LOGS_TABLE} WHERE {ID_F}={record_id}')
        with pytest.raises(InvalidIdException):
            self.mysql.get_record(record_id)


class TestOrmMysql:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client: MysqlOrmClient):
        self.mysql = mysql_orm_client
        mysql_orm_client.create_nginx_logs()

    def test_insert(self, faker: Faker):
        r = LogsRecord.fake(faker)
        print(r)
        record = self.mysql.add_record(r)
        print(record)
        assert self.mysql.has_record(record)
        self.mysql.delete_record(record)
        assert not self.mysql.has_record(record)
