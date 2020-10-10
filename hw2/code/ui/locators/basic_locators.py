from selenium.webdriver.common.by import By
from ui.utils import lowercase_xpath


class BasePageLocators(object):
    LOGO = (By.XPATH, '//a[contains(@class, "head-module-myTargetLogo")]')


class MainPageLocators(BasePageLocators):
    AUTH_POPUP_BUTTON = (By.XPATH, '//div[contains(@class,"responseHead-module-rightSide")]'
                                   '/div[contains(@class,"responseHead-module-button")]')
    AUTH_EMAIL_INPUT = (By.XPATH, '//div[contains(@class,"authForm-module-inputs")]'
                                  '/div[contains(@class,"authForm-module-inputWrap")][last()-1]'
                                  '/input[contains(@class,"authForm-module-input")]')
    AUTH_PASSWD_INPUT = (By.XPATH, '//div[contains(@class,"authForm-module-inputs")]'
                                   '/div[contains(@class,"authForm-module-inputWrap")][last()]'
                                   '/input[contains(@class,"authForm-module-inputPassword")]')
    AUTH_SUBMIT = (By.XPATH, '//div[contains(@class,"authForm-module-button")]')


class DashboardPageLocators(BasePageLocators):
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//div[contains(@class,"dashboard-module-createButtonWrap")]'
                                        '//div[contains(@class, "button-module-textWrapper")]')


class CreateCampaignPageLocators(BasePageLocators):
    TRAFFIC_BUTTON = (By.XPATH, '//div[contains(@class,"_traffic")][@data-class-name="ColumnListItemView"]')
    SOCIAL_ENGAGEMENT_BUTTON = (By.XPATH, '//div[contains(@class,"_socialengagement")]'
                                          '[@data-class-name="ColumnListItemView"]')

    """Locators for input lines"""
    INPUT_LINE = {
        'URL': (By.XPATH, '//input[contains(@class,"suggester-module-searchInput")]'),
        'CAMPAIGN_NAME': (By.XPATH, '//div[contains(@class, "input_campaign-name")]//input'),
        'TOTAL_SUM': (By.XPATH, '//div[contains(@class,"budget-setting__budget")]'
                                '//div[contains(@class,"budget-setting__item-wrap")][last()]'
                                '//input'),
        'SUM_PER_DAY': (By.XPATH, '//div[contains(@class,"budget-setting__budget")]'
                                  '//div[contains(@class,"budget-setting__item-wrap")][last()-1]'
                                  '//input')
    }

    """Locators for tab buttons

    These buttons are used to change tab content
    This tab contains two checkboxes that are used to choose target devices (mobile or desktop)
    """
    TAB_BUTTON = {
        'CAROUSEL': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][1]'),
        'MULTI_FORMAT': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][2]'),
        'SQUARE_VIDEO': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][3]'),
        'HORIZONTAL_VIDEO': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][4]'),
        'FULL_SCREEN_VIDEO': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][5]'),
        'BANNER': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][6]'),
        'TEASER': (By.XPATH, '//div[@data-class-name="BannerFormatItemView"][7]')
    }

    DEVICE_TYPE_CHECKBOX = {
        'MOBILE': (By.XPATH, f'//li[contains({lowercase_xpath(".")},"мобильные")]'
                             '/input[contains(@class,"padItem-module-input")]'),
        'DESKTOP': (By.XPATH, f'//li[contains({lowercase_xpath(".")},"десктопные")]'
                              '/input[contains(@class,"padItem-module-input")]')
    }

    OPTIONS_TAB = (By.XPATH, '//div[contains(@class, "bannerFormats-module-padsWrap")]')
    ADD_BANNER_BUTTON = (By.XPATH, '//div[@data-class-name="BannerForm"]'
                                   '//button[contains(@class,"button_submit")]')

    class Photo256x256:
        ADD_FILE_BUTTON = (By.XPATH, '//div[contains(@class,"input__upload-wrap")]'
                                     '//button[contains(@class,"button_general")]')

        FILE_INPUT = (By.XPATH, '//input[@type="file"]')

    class Photo600x600:
        ADD_FILE_BUTTON = (By.XPATH, '//div[contains(@class,"input__upload-wrap")]'
                                     '//button[contains(@class,"button_general")]')

        FILE_INPUT = (By.XPATH, '//input[@type="file"]')

    # class Photo256x256:
    #     ADD_FILE_BUTTON = (By.XPATH, '//div[contains(@class,"input__upload-wrap")]'
    #                                  '//button[contains(@class,"button_general")]')
    #
    #     FILE_INPUT = (By.XPATH, '//input[@type="file"]')
