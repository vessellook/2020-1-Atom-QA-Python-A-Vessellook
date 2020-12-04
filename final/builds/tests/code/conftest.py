"""The main configuration file for pytest. See also files in pytest_plugins list"""

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from ui.pages.authorization_page import AuthorizationPage
from clients.api_client import ApiClient
from clients.mysql_client import MysqlClient
from settings import Settings

pytest_plugins = ['ui.fixtures', 'clients.fixtures']


def pytest_add_option(parser: Parser):
    parser.addoption('--selenoid-netloc', default='selenoid:4444', help='Host and port for selenoid')
    parser.addoption('--admin-username', default='admin', help="username for admin")
    parser.addoption('--admin-email', default='admin@admin.mail.ru', help="email for admin")
    parser.addoption('--admin-password', default='admin_pass', help="password for admin")
    parser.addoption('--application-netloc', default='proxy:80', help='Host and port for application')
    parser.addoption('--mock-netloc', default='mock:5000', help='Host and port for VK API mock')
    parser.addoption('--mysql-host', default='mysql', help='Host for MySQL server')
    parser.addoption('--mysql-port', default=3306, type=int, help='Port for MySQL server')
    parser.addoption('--mysql-database', default='technoatom', help='Database name')
    parser.addoption('--mysql-table', default='test_users', help='Table in database')
    parser.addoption('--mysql-user', default='test_qa', help='User that admins table in database')
    parser.addoption('--mysql-password', default='qa_test', help='Password for the user')
    parser.addoption('--screenshots-dir', default='/screenshots', help='Dir for screenshots')
    parser.addoption('--video-dir', default='/video', help='Dir for video')
    parser.addoption('--video-enable', const=False, action='store_true',
                     help='Enable video for UI tests with "enable_video" marker')
    parser.addoption('--time-load-page', default=20, help='Max time to load page')
    parser.addoption('--time-input-text', default=20, help='Max time to input some text')


@pytest.fixture(scope='session')
def settings(config: Config):
    return Settings(
        selenoid_netloc=config.getoption('--selenoid-netloc'),
        admin_username=config.getoption('--admin_username'),
        admin_email=config.getoption('--admin_email'),
        admin_password=config.getoption('--admin_password'),
        app_netloc=config.getoption('--application-netloc'),
        mock_netloc=config.getoption('--mock-netloc'),
        mysql_host=config.getoption('--mysql-host'),
        mysql_port=config.getoption('--mysql_port'),
        mysql_database=config.getoption('--mysql-database'),
        mysql_user=config.getoption('--mysql-user'),
        mysql_password=config.getoption('--mysql-password'),
        screenshots_dir=config.getoption('--screenshots-dir'),
        video_dir=config.getoption('--video-dir'),
        video_enable=config.getoption('--video-enable'),
        time_load_page=config.getoption('--time-load-page'),
        time_input_text=config.getoption('--time-input-text')
    )


def pytest_configure(config: Config, settings: Settings, mysql_client: MysqlClient):
    if not hasattr(config, "slaveinput"):
        # executes on master
        mysql_client.add_registered_user(username=settings.admin_username,
                                         email=settings.admin_email,
                                         password=settings.admin_password)

        driver = webdriver.Remote(command_executor=f'http://{settings.selenoid_netloc}/wd/hub/',
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
