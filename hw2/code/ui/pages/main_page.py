from ui.locators.basic_locators import MainPageLocators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class MainPage(BasePage):
    locators = MainPageLocators()
    url = 'http://target.my.com'

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.driver.get(self.url)

    def auth(self, email: str, password: str) -> DashboardPage:
        self.click(self.locators.AUTH_POPUP_BUTTON, 10)

        email_input = self.find(self.locators.AUTH_EMAIL_INPUT)
        email_input.clear()
        email_input.send_keys(email)

        password_input = self.find(self.locators.AUTH_PASSWD_INPUT)
        password_input.clear()
        password_input.send_keys(password)

        submit_button = self.find(self.locators.AUTH_SUBMIT)
        submit_button.click()
        return DashboardPage(self.driver)
