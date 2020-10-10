from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators import basic_locators


class BasePage(object):
    RETRY_COUNT = 3
    locators = basic_locators.BasePageLocators()

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def has(self, locator) -> bool:
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def find(self, locator, timeout=10) -> WebElement:
        """поиск элемента с ожиданием

        кидает исключение StaleElementReferenceException"""
        return self.wait(timeout).until(conditions.presence_of_element_located(locator))

    def click(self, locator, timeout=10):
        # попытки чтобы кликнуть
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

    # def scroll_to_element(self, element):
    #     # нигде не используется, потому что click сам скролит
    #     # просто пример возможной реализации
    #     self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def wait(self, timeout=None) -> WebDriverWait:
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def count_elements(self, locator, count, timeout=1):
        """этот метод считает количество элементов на странице

        until принимает функцию, а значит мы можем написать и использовать свою,
        в нашем случае это lambda функция
        в этом методе мы ожидаем пока не появится нужное нам количество элементов на странице
        """
        self.wait(timeout).until(lambda browser: len(browser.find_elements(*locator)) == count)

    def input(self, locator, text, click: bool = True):
        input_element = self.find(locator, 10)
        if click:
            self.click(locator, 10)
            input_element.clear()
        input_element.send_keys(text)

    def get_title(self) -> str:
        return self.driver.title
