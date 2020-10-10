from ui.locators.basic_locators import CreateCampaignPageLocators
from ui.pages.base_page import BasePage


class CreateCampaignPage(BasePage):
    locators = CreateCampaignPageLocators()

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def is_url_matches(self):
        return 'target.my.com/campaign/new' in self.driver.current_url

    def fill_campaign(self, campaign_name, sum_per_day, total_sum):
        self.input(self.locators.INPUT_LINE['CAMPAIGN_NAME'], campaign_name)
        self.input(self.locators.INPUT_LINE['TOTAL_SUM'], total_sum)
        self.input(self.locators.INPUT_LINE['SUM_PER_DAY'], sum_per_day)

    def social_engagement(self, post_url, campaign_name, sum_per_day, total_sum):
        self.click(self.locators.SOCIAL_ENGAGEMENT_BUTTON, 30)
        self.input(self.locators.INPUT_LINE['URL'], post_url)
        self.fill_campaign(campaign_name, sum_per_day, total_sum)

    def is_mobile_enabled(self):
        return self.find(self.locators.DEVICE_TYPE_CHECKBOX['MOBILE']).is_enabled()

    def is_desktop_enabled(self):
        return self.find(self.locators.DEVICE_TYPE_CHECKBOX['DESKTOP']).is_enabled()

    def traffic(self, site_url, campaign_name, sum_per_day, total_sum):
        self.click(self.locators.TRAFFIC_BUTTON, 30)
        self.input(self.locators.INPUT_LINE['URL'], site_url)
        self.fill_campaign(campaign_name, sum_per_day, total_sum)
        carousel = Carousel(self)
        carousel.choose(mobile=True, desktop=False)
        carousel.add_banner('~/Pictures/img_top.jpg')
        import time
        time.sleep(60)


class Carousel:
    def __init__(self, page: BasePage):
        self.page = page

    def choose(self, mobile=True, desktop=True):
        locators = self.page.locators
        self.page.click(locators.TAB_BUTTON['CAROUSEL'], 10)
        self.page.click(locators.OPTIONS_TAB, 10)
        if self.page.find(locators.MOBILE_TYPE_CHECKBOX, 10).is_selected() != mobile:
            self.page.click(locators.MOBILE_TYPE_CHECKBOX, 10)
        if self.page.find(locators.DESKTOP_TYPE_CHECKBOX, 10).is_selected() != desktop:
            self.page.click(locators.DESKTOP_TYPE_CHECKBOX, 10)
        self.page.click(locators.ADD_BANNER_BUTTON, 10)

    def add_banner(self, file_path):
        self.page.click(self.page.locators.ADD_FILE_BUTTON, 10)
        self.page.input(self.page.locators.FILE_INPUT, file_path)
