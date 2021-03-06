import pytest

from conftest import Settings
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture(scope='function')
def dashboard_page(main_page, settings: Settings):
    email = settings.email
    password = settings.password
    return main_page.auth(email, password)


@pytest.fixture(scope='function')
def create_campaign_page(dashboard_page):
    return dashboard_page.create_campaign()


@pytest.fixture(scope='function')
def segments_page(dashboard_page):
    return dashboard_page.open_segments_page()
