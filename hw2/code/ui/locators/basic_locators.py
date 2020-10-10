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
