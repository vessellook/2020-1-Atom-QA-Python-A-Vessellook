"""The main configuration file for pytest. See also files in pytest_plugins list"""
import time

import pytest
import requests
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from ui.pages.authorization_page import AuthorizationPage
from clients.api_client import ApiClient
from clients.mysql_client import MysqlClient
from settings import Settings

pytest_plugins = ['ui.fixtures', 'clients.fixtures']


def pytest_addoption(parser: Parser):
    parser.addoption('--selenoid-netloc', default='selenoid:4444', help='Host and port for selenoid')
    parser.addoption('--admin-username', default='administrator', help="username for admin")
    parser.addoption('--admin-email', default='admin@admin.mail.ru', help="email for admin")
    parser.addoption('--admin-password', default='admin_pass', help="password for admin")
    parser.addoption('--application-api-netloc', default='proxy:80', help='Host and port for application in api_client')
    parser.addoption('--application-ui-netloc', default='proxy:80', help='Host and port for application in ui Objects')
    parser.addoption('--mock-netloc', default='mock:5000', help='Host and port for VK API mock')
    parser.addoption('--mysql-host', default='mysql', help='Host for MySQL server')
    parser.addoption('--mysql-port', default=3306, type=int, help='Port for MySQL server')
    parser.addoption('--mysql-database', default='technoatom', help='Database name')
    parser.addoption('--mysql-table', default='test_users', help='Table in database')
    parser.addoption('--mysql-user', default='test_qa', help='User that admins table in database')
    parser.addoption('--mysql-password', default='qa_test', help='Password for the user')
    parser.addoption('--screenshots-dir', default='/screenshots', help='Dir for screenshots')
    parser.addoption('--video-dir', default='/video', help='Dir for video')
    parser.addoption('--video-enable', default=False, action='store_true',
                     help='Enable video for UI tests with "enable_video" marker')
    parser.addoption('--time-load-page', default=20, help='Max time to load page')
    parser.addoption('--time-input-text', default=20, help='Max time to input some text')
    parser.addoption('--not-receive-admin-keys', default=False, action='store_true',
                     help="this flag should be used if you don't want to run tests")


@pytest.fixture(scope='session')
def settings(request: FixtureRequest):
    return Settings.from_config(request.config)


def wait_for_it(url, timeout=1, interval=3, retries=10):
    for _ in range(retries):
        try:
            requests.get(url, timeout=timeout)
            break
        except requests.RequestException:
            time.sleep(interval)


def pytest_configure(config: Config):
    normal_start = not config.getoption('--fixtures') and \
                   not config.getoption('--collect-only')
    if not hasattr(config, "workerinput") and normal_start:
        # executes on master
        print('pytest: pytest_configure enter')
        settings = Settings.from_config(config)
        wait_for_it(f'http://{settings.app_api_netloc}/healthcheck')
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
        settings.admin_keys = ApiClient.Keys(session=main_page.session_cookie,
                                             agent=main_page.user_agent)
        driver.quit()
        ApiClient.admin_keys = settings.admin_keys
        ApiClient.netloc = settings.app_api_netloc
        print('pytest: pytest_configure exit')
