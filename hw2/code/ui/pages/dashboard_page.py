from ui.locators.basic_locators import DashboardPageLocators
from ui.pages.base_page import BasePage
from ui.pages.create_campaign_page import CreateCampaignPage


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
        while True:
            if self.has(locator):
                return True
            if not self.find(self.locators.NEXT_PAGINATION_BUTTON_ENABLED, timeout=10).is_enabled():
                break
            self.click(self.locators.NEXT_PAGINATION_BUTTON_ENABLED, timeout=10)
        return False

    def remove_campaign(self, campaign_name: str) -> None:
        self.click(self.locators.get_campaign_settings_button(campaign_name), timeout=10)
        self.click(self.locators.DELETE_CAMPAIGN_BUTTON, timeout=10)
