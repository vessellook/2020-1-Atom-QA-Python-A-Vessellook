from ui.pages.base_page import BasePage
from ui.locators.basic_locators import SegmentsPageLocators
from conftest import ElementNotFoundException


class SegmentsPage(BasePage):
    locators = SegmentsPageLocators()

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def create_segment(self, segment_name: str) -> None:
        if self.has(self.locators.CREATE_SEGMENT_FROM_EMPTY_LIST_LINK):
            self.click(self.locators.CREATE_SEGMENT_FROM_EMPTY_LIST_LINK, timeout=10)
        else:
            self.click(self.locators.CREATE_SEGMENT_FROM_LIST_BUTTON, timeout=10)

        self.click(self.locators.SOCIAL_NETWORK_APPLICATIONS_OPTION, timeout=10)
        self.click(self.locators.ADD_SEGMENT_SOURCE_CHECKBOX, timeout=10)
        self.click(self.locators.ADD_SEGMENT_BUTTON, timeout=10)
        self.input(self.locators.SEGMENT_TITLE, segment_name)
        self.click(self.locators.FINISH_CREATE_SEGMENT_BUTTON, timeout=10)

    def has_segment(self, segment_name: str) -> bool:
        locator = self.locators.get_segment_name_element(segment_name)
        button_locator = self.locators.NEXT_PAGINATION_BUTTON_ENABLED
        while True:
            if self.has(locator, timeout=10):
                return True
            if not self.has(button_locator, timeout=10):
                break
            self.click(button_locator, timeout=10)
        return False

    def remove_segment(self, segment_name: str) -> None:
        locator = self.locators.get_segment_remove_button(segment_name)
        button_locator = self.locators.NEXT_PAGINATION_BUTTON_ENABLED
        while True:
            if self.has(locator, timeout=10):
                self.click(locator, timeout=10)
                self.click(self.locators.CONFIRM_REMOVE_BUTTON, timeout=10)
                return
            if not self.has(button_locator, timeout=10):
                break
            self.click(button_locator, timeout=10)
        raise ElementNotFoundException
