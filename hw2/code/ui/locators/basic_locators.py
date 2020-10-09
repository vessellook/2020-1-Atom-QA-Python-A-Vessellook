from selenium.webdriver.common.by import By


class BasePageLocators(object):
    LOGO = (By.XPATH, '//a[contains(@class, "head-module-myTargetLogo")]')
