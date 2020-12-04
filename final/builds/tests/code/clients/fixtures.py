"""Set of fixtures that are used to connect to test servers"""

import pytest

from clients.api_client import ApiClient
from clients.mock_client import MockClient
from clients.mysql_client import MysqlClient
from settings import Settings


@pytest.fixture(scope='function')
def api_client(settings: Settings):
    """Return `ApiClient` object with valid `Keys`

    You can test API without authorization through web interface each time
    You should use it to test API as authorized user"""
    return ApiClient(admin_keys=settings.admin_keys,
                     netloc=settings.app_netloc)


@pytest.fixture(scope='function')
def mock_client(settings: Settings):
    """Return `MockClient` object that can give instructions to mock server"""
    return MockClient(settings.mock_netloc)


@pytest.fixture(scope='function')
def mysql_client(settings: Settings):
    """Return `MySQLClient` object that can query to MySQL test server"""
    return MysqlClient(db_name=settings.mysql_database, table_name=settings.mysql_table,
                       user=settings.mysql_user, password=settings.mysql_password,
                       host=settings.mysql_host, port=settings.mysql_port)
