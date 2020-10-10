from ui.locators.create_campaign_page_locators import CreateCampaignPageLocators
from ui.pages.base_page import BasePage
import os.path
from ui.pages import dashboard_page


class CreateCampaignPage(BasePage):
    locators = CreateCampaignPageLocators()

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def is_url_matches(self):
        return 'target.my.com/campaign/new' in self.driver.current_url

    def fill_campaign(self, campaign_name: str, sum_per_day: int, total_sum: int):
        self.input(self.locators.INPUT_LINE['CAMPAIGN_NAME'], campaign_name)
        self.input(self.locators.INPUT_LINE['TOTAL_SUM'], total_sum)
        self.input(self.locators.INPUT_LINE['SUM_PER_DAY'], sum_per_day)

    def social_engagement(self, post_url: str, campaign_name: str, sum_per_day: int, total_sum: int):
        self.click(self.locators.SOCIAL_ENGAGEMENT_BUTTON, timeout=10)
        self.input(self.locators.INPUT_LINE['URL'], post_url)
        self.fill_campaign(campaign_name, sum_per_day, total_sum)

    def is_mobile_enabled(self):
        return self.find(self.locators.DEVICE_TYPE_CHECKBOX['MOBILE']).is_enabled()

    def is_desktop_enabled(self):
        return self.find(self.locators.DEVICE_TYPE_CHECKBOX['DESKTOP']).is_enabled()

    def traffic(self,
                site_url: str,
                campaign_name: str,
                sum_per_day: int,
                total_sum: int) -> 'dashboard_page.DashboardPage':
        self.click(self.locators.TRAFFIC_BUTTON, timeout=10)
        self.input(self.locators.INPUT_LINE['URL'], site_url)
        self.fill_campaign(campaign_name, sum_per_day, total_sum)
        carousel = Carousel(self)
        carousel.choose(mobile=True, desktop=False)
        carousel.add_banner('test', os.path.abspath('../res/img.jpg'))
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON, timeout=10)
        return dashboard_page.DashboardPage(self.driver)


class Carousel:
    def __init__(self, page: CreateCampaignPage):
        self.page = page
        self.locators = page.locators.BannerLocators

    def choose(self, mobile: bool = True, desktop: bool = True):
        locators = self.page.locators
        self.page.click(self.locators.TAB_BUTTON['CAROUSEL'], timeout=10)
        self.page.click(self.locators.OPTIONS_TAB, timeout=10)
        if self.page.find(locators.DEVICE_TYPE_CHECKBOX['MOBILE'], timeout=10).is_selected() != mobile:
            self.page.click(locators.DEVICE_TYPE_CHECKBOX['MOBILE'], timeout=10)
        if self.page.find(locators.DEVICE_TYPE_CHECKBOX['DESKTOP'], timeout=10).is_selected() != desktop:
            self.page.click(locators.DEVICE_TYPE_CHECKBOX['DESKTOP'], timeout=10)
        self.page.click(self.locators.ADD_BANNER_BUTTON, timeout=10)

    def add_banner(self, title: str, image_256_path: str, image_600_path: str = None):
        if image_600_path is None:
            image_600_path = image_256_path

        self.page.input(self.locators.PHOTO_256['FILE_INPUT'], image_256_path, click=False)
        self.page.click(self.page.locators.SAVE_PICTURE_BUTTON, timeout=10)
        self.page.input(self.locators.TITLE_INPUT, title)
        self.page.input(self.locators.DESCRIPTION_TEXTAREA, title)

        self.fill_slide(1, title + '|1', image_600_path)
        self.fill_slide(2, title + '|2', image_600_path)
        self.fill_slide(3, title + '|3', image_600_path)

        self.page.click(self.locators.ADD_BANNER_BUTTON, timeout=10)

    def fill_slide(self, slide_num: int, title: str, file_path: str):
        slide_locators = self.locators.SlideLocators(slide_num)
        self.page.click(slide_locators.slide_button, timeout=10)
        self.page.input(slide_locators.file_input, file_path, click=False)
        self.page.click(self.page.locators.SAVE_PICTURE_BUTTON, timeout=10)
        self.page.input(slide_locators.title_input, title)
