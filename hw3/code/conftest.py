import logging
import os
from dataclasses import dataclass

import allure
import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest

from api.my_target_client import MyTargetClient
from variables import PASSWORD, EMAIL


@dataclass
class Settings:
    email: str = None
    password: str = None


def pytest_addoption(parser: Parser):
    parser.addoption('--email', default=EMAIL)
    parser.addoption('--password', default=PASSWORD)


@pytest.fixture(scope='session')
def config(request: FixtureRequest) -> Settings:
    email = request.config.getoption('--email')
    password = request.config.getoption('--password')

    return Settings(email, password)


@pytest.fixture(scope='function')
def logger(request):
    """Фикстура для логирования"""
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = request.node.location[-1]

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    log = logging.getLogger('api_log')
    log.propagate = False
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    failed_count = request.session.testsfailed
    yield log
    if request.session.testsfailed > failed_count:
        with open(log_file, 'r') as file:
            allure.attach(file.read(), name=log.name, attachment_type=allure.attachment_type.TEXT)

    os.remove(log_file)


@pytest.fixture(scope='function')
def my_target_client(config: Settings, logger: logging.Logger):
    client = MyTargetClient(logger, config.email, config.password)
    client.auth()
    return client
