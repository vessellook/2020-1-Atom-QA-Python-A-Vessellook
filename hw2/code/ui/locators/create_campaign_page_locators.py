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
    TRAFFIC_BUTTON = locator(XPATH('div')
                             .add_class('_traffic')
                             .add_attribute(attribute='data-class-name',
                                            value='ColumnListItemView',
                                            strict_match=False))

    SOCIAL_ENGAGEMENT_BUTTON = locator(XPATH('div')
                                       .add_class('_socialengagement')
                                       .add_attribute(attribute='data-class-name',
                                                      value='ColumnListItemView',
                                                      strict_match=False))

    """Locators for input lines"""
    INPUT_LINE = {
        'URL': locator(XPATH('input')
                       .add_class('suggester-module-searchInput')),
        'CAMPAIGN_NAME': locator(XPATH('div')
                                 .add_class('input_campaign-name')
                                 .add_descendant('input')),
        'TOTAL_SUM': locator(XPATH('div')
                             .add_class('budget-setting__budget')
                             .add_descendant('div')
                             .add_class('budget-setting__item-wrap')
                             .add_predicate('[last()]')
                             .add_descendant('input')),
        'SUM_PER_DAY': locator(XPATH('div')
                               .add_class('budget-setting__budget')
                               .add_descendant('div')
                               .add_class('budget-setting__item-wrap')
                               .add_predicate('[last()-1]')
                               .add_descendant('input'))
    }

    DEVICE_TYPE_CHECKBOX = {
        'MOBILE': locator(XPATH('li')
                          .add_predicate(f'[contains({lowercase_xpath(".")},"мобильные")]')
                          .add_descendant('input')
                          .add_class('padItem-module-input')),
        'DESKTOP': locator(XPATH('li')
                           .add_predicate(f'[contains({lowercase_xpath(".")},"десктопные")]')
                           .add_descendant('input')
                           .add_class('padItem-module-input'))
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

        """Locators for tab buttons
    
        These buttons are used to change tab content
        This tab contains two checkboxes that are used to choose target devices (mobile or desktop)
        """
        TAB_BUTTON = {

            'CAROUSEL': locator(XPATH('div')
                                .add_attribute(attribute='data-class-name',
                                               value='BannerFormatItemView',
                                               strict_match=True)
                                .add_num(1)),
            'MULTI_FORMAT': locator(XPATH('div')
                                    .add_attribute(attribute='data-class-name',
                                                   value='BannerFormatItemView',
                                                   strict_match=True)
                                    .add_num(2)),
            'SQUARE_VIDEO': locator(XPATH('div')
                                    .add_attribute(attribute='data-class-name',
                                                   value='BannerFormatItemView',
                                                   strict_match=True)
                                    .add_num(3)),
            'HORIZONTAL_VIDEO': locator(XPATH('div')
                                        .add_attribute(attribute='data-class-name',
                                                       value='BannerFormatItemView',
                                                       strict_match=True)
                                        .add_num(4)),
            'FULL_SCREEN_VIDEO': locator(XPATH('div')
                                         .add_attribute(attribute='data-class-name',
                                                        value='BannerFormatItemView',
                                                        strict_match=True)
                                         .add_num(5)),
            'BANNER': locator(XPATH('div')
                              .add_attribute(attribute='data-class-name',
                                             value='BannerFormatItemView',
                                             strict_match=True)
                              .add_num(6)),
            'TEASER': locator(XPATH('div')
                              .add_attribute(attribute='data-class-name',
                                             value='BannerFormatItemView',
                                             strict_match=True)
                              .add_num(7)),

        }

        OPTIONS_TAB = locator(XPATH('div')
                              .add_class('bannerFormats-module-padsWrap'))
        ADD_BANNER_BUTTON = locator(XPATH('div')
                                    .add_attribute(attribute='data-class-name',
                                                   value='BannerForm',
                                                   strict_match=True)
                                    .add_descendant('button')
                                    .add_class('button_submit'))

        PHOTO_256 = {

            'ADD_BUTTON': locator(XPATH('div')
                                  .add_attribute(attribute='data-class-name',
                                                 value='FileImageView',
                                                 strict_match=True)
                                  .add_predicate('[contains(.,"256")]')
                                  .add_descendant('button')
                                  .add_class('button_general')),

            'FILE_INPUT': locator(XPATH('div')
                                  .add_attribute(attribute='data-class-name',
                                                 value='FileImageView',
                                                 strict_match=True)
                                  .add_predicate('[contains(.,"256")]')
                                  .add_descendant('input')
                                  .add_attribute(attribute='type',
                                                 value='file',
                                                 strict_match=True))
        }
