from selenium.webdriver.common.by import By


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
    pass
