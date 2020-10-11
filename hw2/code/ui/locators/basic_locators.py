from ui.utils import locator, XPATH


class BasePageLocators(object):
    LOGO = locator(XPATH('a')
                   .add_class('head-module-myTargetLogo'))


class MainPageLocators(BasePageLocators):
    AUTH_POPUP_BUTTON = locator(XPATH('div')
                                .add_class('responseHead-module-rightSide')
                                .add_descendant('div')
                                .add_class('responseHead-module-button'))

    AUTH_EMAIL_INPUT = locator(XPATH('div')
                               .add_class('authForm-module-inputs')
                               .add_descendant('div')
                               .add_class('authForm-module-inputWrap')
                               .add_predicate('[last()-1]')
                               .add_descendant('input')
                               .add_class('authForm-module-input'))

    AUTH_PASSWD_INPUT = locator(XPATH('div')
                                .add_class('authForm-module-inputs')
                                .add_descendant('div')
                                .add_class('authForm-module-inputWrap')
                                .add_predicate('[last()]')
                                .add_descendant('input')
                                .add_class('authForm-module-inputPassword'))

    AUTH_SUBMIT = locator(XPATH('div')
                          .add_class('authForm-module-button'))


class DashboardPageLocators(BasePageLocators):
    CREATE_CAMPAIGN_INTRODUCTION_LINK = locator(XPATH('li')
                                                .add_class('instruction-module-item')
                                                .add_descendant('a')
                                                .add_attribute(attribute='href',
                                                               value='/dashboard/new',
                                                               strict_match=False))

    CREATE_CAMPAIGN_BUTTON = locator(XPATH('div')
                                     .add_class('dashboard-module-createButtonWrap')
                                     .add_descendant('div')
                                     .add_class('button-module-textWrapper'))

    DELETE_CAMPAIGN_BUTTON = locator(XPATH()
                                     .add_class('optionsList-module-optionsList')
                                     .add_descendant()
                                     .add_predicate(f'contains({XPATH.lowercase(".")},"удалить")'))

    SEGMENTS_BUTTON = locator(XPATH()
                              .add_class('center-module-segments'))

    NEXT_PAGINATION_BUTTON_ENABLED = locator(XPATH('div')
                                             .add_class('pagination-module-rightBtn')
                                             .disallow_class('button-module-disabled'))

    @staticmethod
    def get_campaign_name_element(campaign_name: str):
        return locator(XPATH('div')
                       .add_class('nameCell-module-campaignNameCell')
                       .add_predicate(f'contains(.,"{campaign_name}")'))

    @staticmethod
    def get_campaign_settings_button(campaign_name: str):
        return locator(XPATH('div')
                       .add_class('nameCell-module-campaignNameCell')
                       .add_predicate(f'contains(.,"{campaign_name}")')
                       .add_parent()
                       .add_following_sibling()
                       .add_num(1)
                       .add_descendant()
                       .add_class('icon-settings'))


class SegmentsPageLocators(BasePageLocators):
    CREATE_SEGMENT_FROM_EMPTY_LIST_LINK = locator((XPATH('div')
                                                   .add_class('page_segments__instruction-wrap')
                                                   .add_predicate('[not(contains(@style,"none"))]')
                                                   .add_descendant('li')
                                                   .add_class('instruction-module-item')
                                                   .add_descendant('a')
                                                   .add_attribute('href',
                                                                  '/segments/segments_list/new/')))

    CREATE_SEGMENT_FROM_LIST_BUTTON = locator((XPATH('div')
                                               .add_class('js-create-button-wrap')
                                               .add_descendant('button')))

    FINISH_CREATE_SEGMENT_BUTTON = locator(XPATH('div')
                                           .add_class('js-create-segment-button-wrap')
                                           .add_descendant('button'))

    SOCIAL_NETWORK_APPLICATIONS_OPTION = locator(XPATH()
                                                 .add_class('adding-segments-item')
                                                 .disallow_class('adding-segments-item_empty')
                                                 .add_predicate(f'contains({XPATH.lowercase(".")},'
                                                                '"приложения и игры в соцсетях")'))

    ADD_SEGMENT_SOURCE_CHECKBOX = locator(XPATH('input')
                                          .add_class('adding-segments-source__checkbox'))

    ADD_SEGMENT_BUTTON = locator(XPATH('div')
                                 .add_class('js-add-button')
                                 .add_descendant('button'))

    SEGMENT_TITLE = locator(XPATH('div')
                            .add_class('input_create-segment-form')
                            .add_descendant('input'))

    NEXT_PAGINATION_BUTTON_ENABLED = locator(XPATH('div')
                                             .add_class('pagination-module-rightBtn')
                                             .disallow_class('button-module-disabled'))

    CONFIRM_REMOVE_BUTTON = locator(XPATH('button')
                                    .add_class('confirm-remove'))

    @staticmethod
    def get_segment_name_element(segment_name: str):
        return locator(XPATH('div')
                       .add_class('main-module-Cell')
                       .add_attribute(attribute='data-test', value='name', strict_match=False)
                       .add_predicate(f'[contains(.,"{segment_name}")]'))

    @staticmethod
    def get_segment_remove_button(segment_name: str):
        return locator(XPATH('div')
                       .add_class('main-module-Cell')
                       .add_attribute(attribute='data-test', value='name', strict_match=False)
                       .add_predicate(f'[contains(.,"{segment_name}")]')
                       .add_following_sibling()
                       .add_attribute(attribute='data-test', value='remove', strict_match=False))
