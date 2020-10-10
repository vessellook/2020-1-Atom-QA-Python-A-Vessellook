from selenium.webdriver.common.by import By
from ui.locators.basic_locators import BasePageLocators
from ui.utils import lowercase_xpath, XPATH, locator


class CreateCampaignPageLocators(BasePageLocators):
    SAVE_PICTURE_BUTTON = locator(XPATH('div')
                                  .add_class('image-cropper')
                                  .add_descendant('input')
                                  .add_class('image-cropper__save'))

    CREATE_CAMPAIGN_BUTTON = locator(XPATH('div')
                                     .add_class('footer__button')
                                     .add_descendant('button')
                                     .add_class('button_submit'))

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
                                  '//input'),
        # 'BANNER_TITLE': (By.XPATH, '//li[contains(@class,"banner-form__field_input")]'
        #                            '[not(contains(@class,"banner-form__field_input_slide-title"))]'
        #                            '//div[contains(@class,"input_title")]'
        #                            '//input'),
        # 'BANNER_DESCRIPTION': (By.XPATH, '//li[contains(@class,"banner-form__field_textarea")]'
        #                                  '[not(contains(@class,"banner-form__field_textarea_slide-text"))]'
        #                                  '//textarea')
    }

    DEVICE_TYPE_CHECKBOX = {
        'MOBILE': (By.XPATH, f'//li[contains({lowercase_xpath(".")},"мобильные")]'
                             '/input[contains(@class,"padItem-module-input")]'),
        'DESKTOP': (By.XPATH, f'//li[contains({lowercase_xpath(".")},"десктопные")]'
                              '/input[contains(@class,"padItem-module-input")]')
    }

    class BannerLocators:
        TITLE_INPUT = locator(XPATH('li')
                              .add_class('banner-form__field_input')
                              .disallow_class('banner-form__field_input_slide-title')
                              .add_descendant('div')
                              .add_class('input_title')
                              .add_descendant('input'))
        DESCRIPTION_TEXTAREA = locator(XPATH('li')
                                       .add_class('banner-form__field_textarea')
                                       .disallow_class('banner-form__field_textarea_slide-text')
                                       .add_descendant('textarea'))

        class SlideLocators:
            def __init__(self, slide_num: int):
                self.slide_num = slide_num

            @property
            def title_input(self):
                return locator(XPATH('li')
                               .add_class('banner-form__field_group_slide-header')
                               .add_num(self.slide_num)
                               .add_descendant('div')
                               .add_class('input_title')
                               .add_descendant('input'))

            @property
            def slide_button(self):
                return locator(XPATH('li')
                               .add_class('banner-form__slides-tabs__item')
                               .add_num(self.slide_num))

            @property
            def add_photo_button(self):
                return locator(XPATH('div')
                               .add_class('banner-form')
                               .add_descendant('li')
                               .add_class('banner-form__field')
                               .add_num(self.slide_num)
                               .add_descendant('button')
                               .add_class('button_general')
                               .add_predicate('contains(.,"600")'))

            @property
            def file_input(self):
                return locator(XPATH('div')
                               .add_class('banner-form')
                               .add_descendant('li')
                               .add_class('banner-form__field')
                               .add_num(self.slide_num)
                               .add_descendant('input')
                               .add_attribute(attribute='type',
                                              value='file',
                                              strict_match=True))
                # 'ADD_BUTTON': (By.XPATH, '//div[contains(@class,"banner-form")]'
                #                          f'//li[contains(@class,"banner-form__field")][{self.slide_num}]'
                #                          '//button[contains(@class,"button_general")][contains(.,"600")]'),
                # 'FILE_INPUT': (By.XPATH, '//div[contains(@class,"banner-form")]'
                #                          f'//li[contains(@class,"banner-form__field")][{self.slide_num}]'
                #                          '//input[@type="file"]')

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

        OPTIONS_TAB = (By.XPATH, '//div[contains(@class, "bannerFormats-module-padsWrap")]')
        ADD_BANNER_BUTTON = (By.XPATH, '//div[@data-class-name="BannerForm"]'
                                       '//button[contains(@class,"button_submit")]')

        PHOTO_256 = {

            'ADD_BUTTON': (By.XPATH, '//div[@data-class-name="FileImageView"][contains(.,"256")]'
                                     '//button[contains(@class,"button_general")]'),
            'FILE_INPUT': (By.XPATH, '//div[@data-class-name="FileImageView"][contains(.,"256")]'
                                     '//input[@type="file"]')

        }
