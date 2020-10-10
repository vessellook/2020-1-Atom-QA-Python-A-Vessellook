from ui.locators.basic_locators import DashboardPageLocators
from ui.pages.base_page import BasePage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.segments_page import SegmentsPage
from conftest import ElementNotFoundException


class DashboardPage(BasePage):
    locators = DashboardPageLocators()

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def create_campaign(self) -> CreateCampaignPage:
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON, timeout=10)
        return CreateCampaignPage(self.driver)

    def is_url_matches(self):
        return 'target.my.com/dashboard' in self.driver.current_url

    def has_campaign(self, campaign_name: str) -> bool:
        locator = self.locators.get_campaign_name_element(campaign_name)
        button_locator = self.locators.NEXT_PAGINATION_BUTTON_ENABLED
        while True:
            if self.has(locator):
                return True
            if not self.find(button_locator, timeout=10).is_enabled():
                break
            self.click(button_locator, timeout=10)
        return False

    def remove_campaign(self, campaign_name: str) -> None:
        while True:
            locator = self.locators.get_campaign_settings_button(campaign_name)
            button_locator = self.locators.NEXT_PAGINATION_BUTTON_ENABLED
            if self.has(locator):
                self.click(locator, timeout=10)
                self.click(self.locators.DELETE_CAMPAIGN_BUTTON, timeout=10)
                return
            if not self.find(button_locator, timeout=10).is_enabled():
                break
            self.click(button_locator, timeout=10)
        raise ElementNotFoundException

    def open_segments_page(self) -> SegmentsPage:
        self.click(self.locators.SEGMENTS_BUTTON, timeout=10)
        return SegmentsPage(self.driver)
