"""The main configuration file for pytest. See also files in pytest_plugins list"""

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest

from settings import Settings

pytest_plugins = ['ui.fixtures', 'clients.fixtures']


def pytest_addoption(parser: Parser):
    parser.addoption('--time-load-page', default=20, type=int, help='Max time to load page')
    parser.addoption('--time-input-text', default=20, type=int, help='Max time to input some text')


@pytest.fixture(scope='session')
def settings(request: FixtureRequest):
    return Settings.from_config(request.config)
