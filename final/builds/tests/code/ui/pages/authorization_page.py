from urllib.parse import urlparse

import allure
import pytest_check as check
from selenium.common.exceptions import WebDriverException

import ui.locators.authorization_page_locators as locators
from ui.pages.base_page import BasePage
from ui.pages import main_page, registration_page


class AuthorizationError(Exception):
    pass


class AuthorizationPage(BasePage):
    urls = ['/', '/login']

    @allure.step("Go to authorization page")
    def make_request(self):
        self.make_request_base(url=f'http://{self.settings.app_netloc}/login')

    @allure.step("Auth with credentials ({username}, {password})")
    def authorize(self, username: str, password: str) -> 'main_page.MainPage':
        self.input(locators.USERNAME_INPUT, text=username)
        self.input(locators.PASSWORD_INPUT, text=password)
        with allure.step('click submit button'):
            self.click(locators.SUBMIT_BUTTON)
            try:
                self.wait(self.load_time).until(main_page.MainPage.is_opened)
            except WebDriverException as e:
                raise AuthorizationError(e.msg)
        return main_page.MainPage(self.driver, self.settings)

    @allure.step("Go to registration page from authorization page")
    def create_an_account(self) -> 'registration_page.RegistrationPage':
        self.click(locators.CREATE_ACCOUNT_LINK)
        self.wait(self.load_time).until(registration_page.RegistrationPage.is_opened)
        return registration_page.RegistrationPage(self.driver, self.settings)

    def check_url(self, msg: str = ''):
        check.is_in(urlparse(self.current_url).path, ('/', '/login'), msg)

    @staticmethod
    def is_opened(driver):
        return urlparse(driver.current_url).path in ('/', '/login')
