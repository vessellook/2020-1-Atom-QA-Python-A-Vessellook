from urllib.parse import urlparse

import allure
import pytest_check as check
from selenium.common.exceptions import WebDriverException

import ui.locators.registration_page_locators as locators
from ui.pages.base_page import BasePage
from ui.pages import main_page, authorization_page


class RegistrationError(Exception):
    pass


class RegistrationPage(BasePage):
    def make_request(self):
        self.make_request_base(url=f'http://{self.settings.app_ui_netloc}/reg')

    @allure.step("Register with credentials ({username}, {email}, {password})")
    def pass_registration(self, username: str, email: str,
                          password: str, confirm_password: str = None) -> 'main_page.MainPage':
        confirm_password = confirm_password if confirm_password is not None else password
        self.input(locators.USERNAME_INPUT, text=username, timeout=60)
        self.input(locators.EMAIl_INPUT, text=email)
        self.input(locators.PASSWORD_INPUT, text=password)
        self.input(locators.CONFIRM_PASSWORD_INPUT, text=confirm_password)
        self.click(locators.TERM_CHECKBOX)
        with allure.step('click submit button'):
            allure.attach.file(
                self.make_screenshot(f'pass_registration-username={username}-click.png'),
                name='before click',
                attachment_type=allure.attachment_type.PNG)
            self.click(locators.SUBMIT_BUTTON)
            try:
                self.wait(self.load_time).until(main_page.MainPage.is_opened)
            except WebDriverException as err:
                if self.has(locators.WARNING_TAG):
                    allure.attach(self.find(locators.WARNING_TAG).text,
                                  name='warning',
                                  attachment_type=allure.attachment_type.TEXT)
                allure.attach.file(
                    self.make_screenshot(f'pass_registration-username={username}-except.png'),
                    name='in except block',
                    attachment_type=allure.attachment_type.PNG)
                raise RegistrationError from err
        return main_page.MainPage(self.driver, self.settings)

    @allure.step("Go to authorization page from registration page")
    def go_to_authorization_page(self) -> 'authorization_page.AuthorizationPage':
        self.click(locators.LOG_IN_LINK)
        self.wait(self.load_time).until(authorization_page.AuthorizationPage.is_opened)
        return authorization_page.AuthorizationPage(self.driver, self.settings)

    def check_url(self, msg: str = ''):
        check.equal(urlparse(self.current_url).path, '/reg', msg)

    @staticmethod
    def is_opened(driver):
        return urlparse(driver.current_url).path == '/reg'
