from typing import List, TextIO

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest

from mysql_client.mysql_client import MysqlClient
from mysql_orm_client.mysql_orm_client import MysqlOrmClient

from names import RAW_QUERIES_DB, ORM_QUERIES_DB


def pytest_addoption(parser: Parser):
    parser.addoption('--port', type=int, default=3306, help='MySQL port')


@pytest.fixture(scope='session')
def logs_list(request: FixtureRequest) -> List[TextIO]:
    logs_files = request.config.getoption('--logs-path')
    yield logs_files
    for file in logs_files:
        file.close()


@pytest.fixture(scope='session')
def config(request: FixtureRequest):
    port = request.config.getoption('--port')
    return {'port': port}


@pytest.fixture(scope='session')
def mysql_client(config):
    return MysqlClient(user='root', password='pass', db_name=RAW_QUERIES_DB, port=config['port'])


@pytest.fixture(scope='session')
def mysql_orm_client(config):
    return MysqlOrmClient(user='root', password='pass', db_name=ORM_QUERIES_DB, port=config['port'])
