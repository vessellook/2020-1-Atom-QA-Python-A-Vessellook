from dataclasses import dataclass
from typing import Optional

from clients.api_client import ApiClient

TABLENAME = 'test_users'


@dataclass
class Settings:
    selenoid_netloc: str
    admin_username: str
    admin_email: str
    admin_password: str
    app_netloc: str
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
    admin_keys: Optional[ApiClient.Keys] = None
