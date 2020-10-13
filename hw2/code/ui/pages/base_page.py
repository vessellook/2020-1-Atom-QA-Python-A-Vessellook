from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.basic_locators import BasePageLocators


class BasePage:
    RETRY_COUNT = 3
    locators = BasePageLocators()

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def has(self, locator, timeout=10) -> bool:
        try:
            self.find(locator, timeout=timeout)
        except StaleElementReferenceException:
            return False
        except TimeoutException:
            return False
        return True

    def find(self, locator, timeout=10) -> WebElement:
        """поиск элемента с ожиданием

        кидает исключение StaleElementReferenceException"""
        return self.wait(timeout).until(conditions.presence_of_element_located(locator))

    def refresh(self):
        import time
        time.sleep(10)
        self.driver.refresh()

    def click(self, locator, timeout=10):
        for i in range(self.RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(conditions.element_to_be_clickable(locator))
                element.click()
                return

            except StaleElementReferenceException:
                if i < self.RETRY_COUNT - 1:
                    pass
        raise

    def wait(self, timeout=None) -> WebDriverWait:
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    def input(self, locator, text, timeout: int = 10, click: bool = True):
        input_element = self.find(locator, timeout)
        if click:
            self.click(locator, timeout)
            input_element.clear()
        input_element.send_keys(text)

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def url(self):
        return self.driver.current_url
