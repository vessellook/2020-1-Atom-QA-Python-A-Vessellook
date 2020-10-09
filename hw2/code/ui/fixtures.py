from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
import pytest


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver=driver)
