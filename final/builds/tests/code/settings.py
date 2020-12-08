from dataclasses import dataclass

from dotenv import dotenv_values
from _pytest.config import Config

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
    time_load_page: int
    time_input_text: int

    @staticmethod
    def from_config(config: Config):
        try:
            envs = dotenv_values(config.rootpath.joinpath('.env'))
            try:
                # load another .env file inside docker container
                # this .env file is created by bash script 'run_in_docker.sh'
                envs.update(dotenv_values(config.rootpath.joinpath('override.env')))
            except OSError:
                pass
            envs.setdefault("SELENOID_HOST", "127.0.0.1")
            envs.setdefault("ADMIN_USERNAME", 'administrator')
            envs.setdefault("ADMIN_EMAIL", 'admin@admin.mail.ru')
            envs.setdefault("ADMIN_PASSWORD", 'admin@admin.mail.ru')
            envs.setdefault("ADMIN_PASSWORD", 'admin_pass')
            envs.setdefault("PROXY_HOST_UI", envs.get("COMPOSE_PROXY_IP_ADDRESS"))
            envs.setdefault("PROXY_HOST_API", "127.0.0.1")
            envs.setdefault("MOCK_HOST", "127.0.0.1")
            envs.setdefault("MYSQL_HOST", "127.0.0.1")
            envs.setdefault("SCREENSHOTS_DIR", f'{envs.get("PROJECT_PATH")}/mount/screenshots')
            envs.setdefault("VIDEO_DIR", f'{envs.get("PROJECT_PATH")}/mount/videos')
        except Exception as err:
            raise Exception('Look at .env file and settings.py') from err
        return Settings(
            selenoid_url=f'http://{envs.get("SELENOID_HOST")}:{envs.get("SELENOID_PORT")}/wd/hub',
            admin_username=envs.get('ADMIN_USERNAME'),
            admin_email=envs.get('ADMIN_EMAIL'),
            admin_password=envs.get('ADMIN_PASSWORD'),
            app_ui_netloc=f'{envs.get("PROXY_HOST_UI")}:80',
            app_api_netloc=f'{envs.get("PROXY_HOST_API")}:{envs.get("PROXY_PORT")}',
            mock_netloc=f'{envs.get("MOCK_HOST")}:{envs.get("MOCK_PORT")}',
            mysql_host=envs.setdefault("MYSQL_HOST"),
            mysql_port=int(envs.get("MYSQL_PORT")),
            mysql_database='technoatom',
            mysql_user='test_qa',
            mysql_password='qa_test',
            screenshots_dir=envs.get("SCREENSHOTS_DIR"),
            video_dir=envs.get("VIDEO_DIR"),
            video_enable=envs.get('VIDEO_ENABLE', '-') == '+',
            time_load_page=config.getoption('--time-load-page'),
            time_input_text=config.getoption('--time-input-text')
        )
