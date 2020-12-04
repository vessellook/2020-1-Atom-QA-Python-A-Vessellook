from typing import Tuple

from selenium.webdriver.common.by import By

LOGOUT_LINK = By.XPATH, '//a[text()="Logout"]'

CITATION_TAG = By.XPATH, '//footer//p[not(contains(text(),"ТЕХНОАТОМ"))]'

LOGGED_AS_TAG = By.XPATH, '//div[@id="login-name"]//*[contains(text(), "Logged as")]'

VK_ID_TAG = By.XPATH, '//div[@id="login-name"]//*[contains(text(), "VK ID:")]'


class LINKS:
    API: Tuple[str, str] = By.XPATH, '//div[text()="What is an API?"]/following-sibling::*/a'
    CENTOS: Tuple[str, str] = By.XPATH, '//a[text()="Download Centos7"]'
    FLASK = By.XPATH, '//a[text()="About Flask"]'
    FUTURE = By.XPATH, '//div[text()="What is an API?"]/following-sibling::*/a'
    HOME = By.XPATH, '//a[text()="HOME"]'
    LOGO = By.XPATH, '//a[text()=" TM version 0.1"]'
    LOGOUT = By.XPATH, '//a[contains(@href, "logout")]'
    LINUX: Tuple[str, str] = By.XPATH, '//a[text()="Linux"]'
    NETWORK = By.XPATH, '//a[text()="Network"]'
    PYTHON = By.XPATH, '//a[text()="Python"]'
    PYTHON_HISTORY = By.XPATH, '//a[text()="Python history"]'
    SMTP = By.XPATH, '//div[text()="Lets talk about SMTP?"]/following-sibling::*/a'
    TCPDUMP_EXAMPLES = By.XPATH, '//*[contains(text(), "Tcpdump")]//a'
    WIRESHARK_NEWS = By.XPATH, '//*[contains(text(),"Wireshark")]//a[text()="News"]'
    WIRESHARK_DOWNLOAD = By.XPATH, '//*[contains(text(),"Wireshark")]//a[text()="Download"]'
