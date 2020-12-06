"""Set of fixtures that are used to connect to test servers"""

import pytest
from filelock import FileLock
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from clients.api_client import ApiClient, Keys
from clients.mock_client import MockClient
from clients.mysql_client import MysqlClient
from settings import Settings

# https://pypi.org/project/pytest-xdist/
from ui.pages.authorization_page import AuthorizationPage


def _admin_keys(settings: Settings):
    mysql_client = MysqlClient(settings)
    mysql_client.clean()
    mysql_client.add_registered_user(
        username=settings.admin_username,
        email=settings.admin_email,
        password=settings.admin_password)
    driver = webdriver.Remote(command_executor=settings.selenoid_url,
                              options=ChromeOptions(),
                              desired_capabilities={'acceptInsecureCerts': True})
    driver.maximize_window()
    authorization_page = AuthorizationPage(driver, settings)
    authorization_page.make_request()
    main_page = authorization_page.authorize(username=settings.admin_username,
                                             password=settings.admin_password)
    keys = Keys(session=main_page.session_cookie,
                          agent=main_page.user_agent)
    driver.quit()
    return keys


@pytest.fixture(scope='session')
def admin_keys(tmp_path_factory, settings: Settings, worker_id):
    if worker_id == 'master':
        return _admin_keys(settings)

    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    path = root_tmp_dir / 'admin_keys.txt'
    with FileLock(str(path) + '.lock'):
        if path.is_file():
            keys_str = path.read_text().splitlines()
            keys = Keys(session=keys_str[0], agent=keys_str[1])
        else:
            keys = _admin_keys(settings)
            path.write_text(f'{keys.session}\n{keys.agent}')
        return keys


@pytest.fixture(scope='function')
def api_client(settings: Settings, admin_keys: Keys):
    """Return `ApiClient` object with valid `Keys`

    You can test API without authorization through web interface each time
    You should use it to test API as authorized user"""
    ApiClient.netloc = settings.app_api_netloc
    ApiClient.admin_keys = admin_keys
    return ApiClient()


@pytest.fixture(scope='function')
def mock_client(settings: Settings):
    """Return `MockClient` object that can give instructions to mock server"""
    return MockClient(settings.mock_netloc)


@pytest.fixture(scope='function')
def mysql_client(settings: Settings):
    """Return `MySQLClient` object that can query to MySQL test server"""
    return MysqlClient(settings)
