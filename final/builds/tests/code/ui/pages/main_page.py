from typing import Optional
from urllib.parse import urlparse

import allure
from selenium.common.exceptions import StaleElementReferenceException

import ui.locators.main_page_locators as locators
from ui.pages.base_page import BasePage
from ui.pages import authorization_page


class MainPage(BasePage):
    locators = locators

    def make_request(self):
        self.make_request_base(url=f'http://{self.settings.app_ui_netloc}/welcome')

    @allure.step("Logout (website redirect you to authorization page)")
    def logout(self) -> 'authorization_page.AuthorizationPage':
        self.click(locators.LOGOUT_LINK)
        self.wait(self.load_time).until(authorization_page.AuthorizationPage.is_opened)
        return authorization_page.AuthorizationPage(self.driver, self.settings)

    @property
    def wisdom_citation(self) -> str:
        return self.find(locators.CITATION_TAG).text

    @property
    def username(self) -> str:
        return self.find(locators.LOGGED_AS_TAG).text[len("Logged as "):]

    @property
    def vk_id(self) -> Optional[str]:
        try:
            return self.find(locators.VK_ID_TAG).text[len('VK ID: '):]
        except StaleElementReferenceException:
            return None

    def check_url(self, msg: str = ''):
        assert 'welcome' in urlparse(self.driver.current_url).path, msg

    def check_url_negative(self, msg: str = ''):
        assert 'welcome' not in urlparse(self.driver.current_url).path, msg


    @staticmethod
    def is_opened(driver):
        return 'welcome' in urlparse(driver.current_url).path
