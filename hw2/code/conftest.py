from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from urllib.parse import urlparse

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest

from variables import EMAIL, PASSWORD
from ui.fixtures import *

def pytest_addoption(parser: Parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='latest')
    parser.addoption('--selenoid', default=None,
                     help="parameter format: --selenoid='host:port'. Default is None")
    parser.addoption('--email', default=EMAIL, help=f'email to log in. Default is {EMAIL}')
    parser.addoption('--password', default=PASSWORD, help=f'password to log in. Default is {PASSWORD}')


@pytest.fixture(scope='session')
def config(request: FixtureRequest):
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')
    email = request.config.getoption('--email')
    password = request.config.getoption('--password')

    if selenoid:
        selenoid = urlparse(selenoid).hostname, urlparse(selenoid).port

    return {
        'browser': browser,
        'version': version,
        'download_dir': '/tmp.txt',
        'selenoid': selenoid,
        'email': email,
        'password': password
    }


class UnsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    download_dir = config['download_dir']
    selenoid = config['selenoid']

    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument("--window-size=800,600")

        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option('prefs', prefs)

        if selenoid:
            driver = webdriver.Remote(command_executor=f'http://{selenoid[0]}:{selenoid[1]}/wd/hub/',
                                      options=options,
                                      desired_capabilities={'acceptInsecureCerts': True}
                                      )
        else:
            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(),
                                      options=options,
                                      desired_capabilities={'acceptInsecureCerts': True}
                                      )

    elif browser == 'firefox':
        manager = GeckoDriverManager(version=version)
        driver = webdriver.Firefox(executable_path=manager.install())

    else:
        raise UnsupportedBrowserException(f'Unsupported browser: "{browser}"')

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request):
    browser = request.param

    if browser == 'chrome':
        manager = ChromeDriverManager(version='latest')
        driver = webdriver.Chrome(executable_path=manager.install())

    elif browser == 'firefox':
        manager = GeckoDriverManager(version='latest')
        driver = webdriver.Firefox(executable_path=manager.install())

    else:
        raise UnsupportedBrowserException(f'Unsupported browser: "{browser}"')

    driver.maximize_window()
    yield driver
    driver.quit()
