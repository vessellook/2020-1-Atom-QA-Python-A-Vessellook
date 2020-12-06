from dataclasses import dataclass
from typing import Optional

from _pytest.config import Config

from clients.api_client import Keys

TABLENAME = 'test_users'


@dataclass
class Settings:
    selenoid_url: str
    admin_username: str
    admin_email: str
    admin_password: str
    app_ui_netloc: str
    app_api_netloc: str
    mock_netloc: str
    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_password: str
    screenshots_dir: str
    video_dir: str
    video_enable: bool
    time_load_page: str
    time_input_text: str

    @staticmethod
    def from_config(config: Config):
        print('[LOOK_T_ME] CONFIG IN SETTINGS', dir(config))
        return Settings(
            selenoid_url=f'http://{config.getoption("--selenoid-netloc")}/wd/hub',
            admin_username=config.getoption('--admin-username'),
            admin_email=config.getoption('--admin-email'),
            admin_password=config.getoption('--admin-password'),
            app_ui_netloc=config.getoption('--application-ui-netloc'),
            app_api_netloc=config.getoption('--application-api-netloc'),
            mock_netloc=config.getoption('--mock-netloc'),
            mysql_host=config.getoption('--mysql-host'),
            mysql_port=config.getoption('--mysql-port'),
            mysql_database=config.getoption('--mysql-database'),
            mysql_user=config.getoption('--mysql-user'),
            mysql_password=config.getoption('--mysql-password'),
            screenshots_dir=config.getoption('--screenshots-dir'),
            video_dir=config.getoption('--video-dir'),
            video_enable=config.getoption('--video-enable'),
            time_load_page=config.getoption('--time-load-page'),
            time_input_text=config.getoption('--time-input-text'),
        )
