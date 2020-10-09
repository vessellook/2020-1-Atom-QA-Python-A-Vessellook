from ui.locators.basic_locators import CreateCampaignPageLocators
from ui.pages.base_page import BasePage


class CreateCampaignPage(BasePage):
    locators = CreateCampaignPageLocators()

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def is_url_matches(self):
        return 'target.my.com/campaign/new' in self.driver.current_url
