from dataclasses import dataclass
from typing import Any

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest

from variables import EMAIL, PASSWORD

pytest_plugins = 'ui.fixtures'


def pytest_addoption(parser: Parser):
    parser.addoption('--browser', default='chrome',
                     help='browser to use in tests. Available values are: chrome, firefox')
    parser.addoption('--browser_ver', default='latest')
    parser.addoption('--selenoid', default='',
                     help="parameter format: --selenoid='host:port'. Default is None")
    parser.addoption('--email', default=EMAIL, help=f'email to log in. Default is {EMAIL}')
    parser.addoption('--password',
                     default=PASSWORD,
                     help=f'password to log in. Default is {PASSWORD}')
    parser.addoption('--headless', default=False,
                     help="pass '--headless True' to start browser in headless mode")


@dataclass
class Settings:
    browser: str = 'chrome'
    version: str = 'latest'
    selenoid: Any = None
    email: str = EMAIL
    password: str = PASSWORD
    headless: bool = True
    download_dir: str = '/tmp'


@pytest.fixture(scope='session')
def settings(request: FixtureRequest) -> Settings:
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid_opt: str = request.config.getoption('--selenoid')
    email = request.config.getoption('--email')
    password = request.config.getoption('--password')
    headless = request.config.getoption('--headless')

    if headless == 'True':
        headless = True
    else:
        headless = False

    selenoid = None

    if selenoid_opt:
        pos = selenoid_opt.rfind(':')
        selenoid = selenoid_opt[:pos], int(selenoid_opt[pos + 1:])

    return Settings(browser=browser,
                    version=version,
                    selenoid=selenoid,
                    email=email,
                    password=password,
                    headless=headless
                    )


class UnsupportedBrowserException(Exception):
    pass


class ElementNotFoundException(Exception):
    pass


class AuthFailedException(Exception):
    pass


@pytest.fixture(scope='function')
def driver(settings: Settings):
    browser = settings.browser
    version = settings.version
    download_dir = settings.download_dir
    selenoid = settings.selenoid
    headless = settings.headless

    if browser == 'chrome':
        options = ChromeOptions()
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option('prefs', prefs)
    elif browser == 'firefox':
        options = FirefoxOptions()
    else:
        raise UnsupportedBrowserException(f'Unsupported browser: "{browser}"')

    options.headless = headless
    if selenoid:
        host, port = selenoid
        driver = webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub/',
                                  options=options,
                                  desired_capabilities={'acceptInsecureCerts': True}
                                  )
    else:

        if browser == 'chrome':
            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(),
                                      options=options,
                                      desired_capabilities={'acceptInsecureCerts': True}
                                      )

        elif browser == 'firefox':
            manager = GeckoDriverManager(version=version)
            driver = webdriver.Firefox(executable_path=manager.install(),
                                       options=options,
                                       desired_capabilities={'acceptInsecureCerts': True}
                                       )
        else:
            raise UnsupportedBrowserException(f'Unsupported browser: "{browser}"')

    driver.maximize_window()
    yield driver
    driver.quit()
