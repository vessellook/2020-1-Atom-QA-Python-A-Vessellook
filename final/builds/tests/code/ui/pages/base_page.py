import time
from typing import Optional

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.wait import WebDriverWait

from settings import Settings


class BasePage:
    RETRY_COUNT = 3

    def __init__(self, driver: WebDriver, settings: Settings):
        self.driver = driver
        self.settings = settings
        self.load_time = settings.time_load_page
        self.input_time = settings.time_input_text
        self.screenshots_dir = settings.screenshots_dir

    def make_request_base(self, url):
        if self.driver.current_url != url:
            html = self.find((By.TAG_NAME, 'html'))
            self.driver.get(url)
            self.wait(self.load_time).until(conditions.staleness_of(html))

    def has(self, locator, timeout=20) -> bool:
        try:
            self.find(locator, timeout=timeout if timeout is not None else 20)
        except StaleElementReferenceException:
            return False
        except TimeoutException:
            return False
        return True

    def find(self, locator, timeout=20) -> WebElement:
        """поиск элемента с ожиданием
        кидает исключение StaleElementReferenceException"""
        return self.wait(timeout=timeout if timeout is not None else 20).until(
            conditions.presence_of_element_located(locator))

    def refresh(self):
        html = self.driver.find_element_by_tag_name('html')
        self.driver.refresh()
        self.wait(self.load_time).until(conditions.staleness_of(html))

    def click(self, locator, timeout=20):
        for _ in range(self.RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout=timeout if timeout is not None else 20).until(
                    conditions.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                pass
        raise StaleElementReferenceException

    def wait(self, timeout=None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=timeout if timeout is not None else 20)

    @allure.step("Input text {text} in element {locator}")
    def input(self, locator, text, timeout: int = 30, click: bool = True):
        input_element = self.find(locator, timeout)
        if click:
            self.click(locator, timeout)
            input_element.clear()
        input_element.send_keys(text)
        if len(text) > 0:
            self.wait(self.input_time).until(
                conditions.text_to_be_present_in_element_value(locator, text))

    def make_screenshot(self, name):
        path = f'{self.screenshots_dir}/{name}--{time.time()}.png'
        self.driver.save_screenshot(path)
        return path

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def session_cookie(self) -> Optional[str]:
        try:
            return self.driver.get_cookie('session')['value']
        except WebDriverException:
            pass

    @property
    def user_agent(self):
        return self.driver.execute_script("return navigator.userAgent;")

    @property
    def source(self):
        return self.driver.page_source
