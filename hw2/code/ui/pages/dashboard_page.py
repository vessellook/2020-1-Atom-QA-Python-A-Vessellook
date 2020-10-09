from ui.locators.basic_locators import DashboardPageLocators
from ui.pages.base_page import BasePage
from ui.pages.create_campaign_page import CreateCampaignPage


class DashboardPage(BasePage):
    locators = DashboardPageLocators()

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def create_campaign(self) -> CreateCampaignPage:
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON, 10)
        return CreateCampaignPage(self.driver)

    def is_url_matches(self):
        return 'target.my.com/dashboard' in self.driver.current_url
