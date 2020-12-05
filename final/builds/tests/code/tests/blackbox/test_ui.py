"""Tests for WEB interface of myapp"""
from urllib.parse import urljoin

import allure
import pytest
# Functions in this package works as operator assert but not stop execution
import pytest_check as check
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import requests

from utils.citations import wisdom_citations
from utils.common import change_netloc
from settings import Settings
from ui.pages.registration_page import RegistrationPage, RegistrationError
from ui.pages.authorization_page import AuthorizationPage, AuthorizationError
from ui.pages.main_page import MainPage
from ui.pages.base_page import BasePage
from clients.mock_client import MockClient
from utils import make


def get_sources_from_page(page: BasePage):
    """Collect source links from page and return absolute URLs

    Source links are links to scripts, stylesheets and images"""
    current_url = page.current_url
    html = BeautifulSoup(page.source, 'html.parser')
    style_urls = [link.get('href') for link in html.find_all('link')
                  if link.get('rel') == 'stylesheet']
    script_urls = [script.get('src') for script in html.find_all('script')]
    img_urls = [img.get('src') for img in html.find_all('img')]
    urls = style_urls + script_urls + img_urls
    return {urljoin(current_url, url) for url in urls if url is not None}


def get_urls_from_page(page: BasePage):
    """Collect urls to another pages and return absolute URLs"""
    html = BeautifulSoup(page.source, 'html.parser')
    urls = [a.get('href') for a in html.find_all('a')]
    return [url for url in urls if url is not None]


@allure.step('Check sources existence: {page_name}')
def check_all_sources_exist(page: BasePage, page_name, msg=''):
    urls = get_sources_from_page(page)
    cookies = {'session': page.session_cookie}
    headers = {'User-Agent': page.user_agent}

    allure.attach(str(urls), name=f'sources_of_{page_name}.txt',
                  attachment_type=allure.attachment_type.TEXT)
    all_right = True
    for url in urls:
        try:
            with allure.step(f'Check url {url}'):
                # allure step to check single url
                response = requests.get(change_netloc(url, page.settings.app_api_netloc),
                                        cookies=cookies, headers=headers, timeout=1)
                assert response.status_code == 200
        except AssertionError:
            all_right = False
    if not all_right:
        raise AssertionError(msg)


class TestUrls:
    """Tests that check urls of pages and links from pages"""

    @pytest.fixture(scope="function")
    def main_page(self, registration_page: RegistrationPage):
        username, email, password = make.auth_data()
        return registration_page.pass_registration(username=username, email=email,
                                                   password=password)

    @pytest.mark.UI
    def test_source_links(self, authorization_page: AuthorizationPage):
        with check.check:
            check_all_sources_exist(authorization_page, 'authorization page',
                                    'some urls are invalid')
        registration_page = authorization_page.create_an_account()
        with check.check:
            check_all_sources_exist(registration_page, 'registration page',
                                    'some urls are invalid')
        username, email, password = make.auth_data()
        main_page = registration_page.pass_registration(username=username, email=email,
                                                        password=password)
        with check.check:
            check_all_sources_exist(main_page, 'main page', 'some urls are invalid')

    @pytest.mark.UI
    def test_current_urls(self, authorization_page: AuthorizationPage):
        authorization_page.check_url('wrong url')
        registration_page = authorization_page.create_an_account()
        registration_page.check_url('wrong url')
        username, email, password = make.auth_data()
        allure.attach(str(username), name='username', attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(email), name='email', attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(password), name='password', attachment_type=allure.attachment_type.TEXT)
        main_page = registration_page.pass_registration(username=username, email=email,
                                                        password=password)
        main_page.check_url('wrong url')


class TestRegistrationPage:
    """Tests for registration page"""

    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        ('6rFcj5GggMNjX', 'g2sZpzqUZtI634E@IVYsE2RHtJmoav1FFD.ky', 'iC40jqbDbuZ9TEpFPG5'),
        ('sXbNYdt2vBXs', 'sZfySbvq4iep9@REhG3Hd0R.ZY', 'JOCBrJt6v7n'),
        ('PfaaufAVN5sH', 'nkTTZrLphw6@corp.mail.ru', 'Ph3Bjgjgg9FZlkDtbeB'),
    ])
    def test_registration_positive(self, username, email, password,
                                   registration_page: RegistrationPage):
        main_page = registration_page.pass_registration(username=username, email=email,
                                                        password=password)
        main_page.check_url()

    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'email', 'password', 'confirm_password'], [
        pytest.param("8oBuKCBjubbdAq0unATM", "fGF9j6hmGar6L5x8qh@qSUeSqbf2NCJFXH.BEXBK", "", "",
                     id="empty password"),
        pytest.param("ImEoIEXslGC4CQzjeY", "", "vPaabADfuox85rCejk2", "vPaabADfuox85rCejk2",
                     id="empty email"),
        pytest.param("", "J1a7tJ9OTroR@9cRcnBrRO2osvxYTGCwP.5Pq", "wca9Nq6nRvQ4a",
                     "wca9Nq6nRvQ4a", id="empty username"),
        pytest.param("UKw6W14l2X", "LQWAV60ezZajuSglw@", "Ti4f1HLPcv54YdGSXR0",
                     "Ti4f1HLPcv54YdGSXR0", id="email without domain"),
        pytest.param("5gt8Huat876", "@QFVi9Sux4ORLtGvXjacS.n1qJ9", "yuXsKBZEheQbu",
                     "yuXsKBZEheQbu", id="email without login"),
        pytest.param("vaYIvsscN6Ld2", "82kzhSd4BRt4p.ru", "kCovCZHwbjtDpYJ", "kCovCZHwbjtDpYJ",
                     id="email without login@"),
        pytest.param("LMY0vbDJmbH", "YmPZAxb1Mo@.ru", "AjgBBf15URzpigvG4v", "AjgBBf15URzpigvG4v",
                     id="email with invalid domain"),
        pytest.param("4KNF55cU0jCf0b55ZFJB", "DCXx9zme2F1JyYFA@mail.", "ztZWdHH7WI2wLVOp",
                     "ztZWdHH7WI2wLVOp", id="invalid email domain"),
        pytest.param("UsLvtJ5rl4w14s6kk", "JJ95MIeidp", "7bohe8wp5hicTdY", "7bohe8wp5hicTdY",
                     id="invalid email"),
        pytest.param("ifHIvjw3xVPObKpMDa8", "WGUrWOpRSM9o@zljozrCAM2fnuCWPaY7.74",
                     "YGilUPG3ahzPVQ", "YGilUPG3ahzPVQ", id="numeric email"),
        pytest.param("pdu2ALdqdWfiEbpCFdtm", "qnfifhySLo4Ax@CzCsYWNxatZfBF.ae3Gd",
                     "gf4bQ0S4OfsrLol", "", id="empty confirm_password field"),
        pytest.param("QtdMZta7n3eOKdNYud", "0r5z1FwkHqlA9r@cf9J06xwQnMCbIWrp.tuoZq",
                     "f6MmP827OKqPHdF", "not equal",
                     id="confirm_password field and password are different")])
    def test_registration_negative(self, username, email, password, confirm_password,
                                   registration_page: RegistrationPage):
        with pytest.raises((AssertionError, RegistrationError)):  # noqa:
            main_page = registration_page.pass_registration(username=username, email=email,
                                                            password=password,
                                                            confirm_password=confirm_password)
            main_page.check_url_negative()


class TestAuthorizationPage:
    """Tests for authorization page"""

    @allure.title('authorization positive')
    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('wk33NtzvQHW3kHMs', 'U3Aje@Kr0poHTbe.0rFu', 'XkJWFH98GhJgvNdg'),
        pytest.param('AKMQsi9PXLFgFTK3', 'EYXMuKMMy@tTVe3KMy.UiaNV', 'vIHt04gINlGf1X3')
    ])
    def test_authorization_positive(self, username, email, password,
                                    registration_page: RegistrationPage):
        main_page = registration_page.pass_registration(username=username, email=email,
                                                        password=password)
        authorization_page = main_page.logout()
        authorization_page.authorize(username=username, password=password)
        allure.attach.file(main_page.make_screenshot('test_authorization_positive'),
                           attachment_type=allure.attachment_type.PNG)
        main_page.check_url()

    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'password'], [
        ('admin', 'admin'),
        ('BILTZ6cWpqaLwO6', 'Gjh3LcpSR4Yl'),
        pytest.param('my-cool-username', '', id='empty password'),
        pytest.param('', 'my-cool-password', id='empty username'),
    ])
    def test_authorization_negative(self, username, password,
                                    authorization_page: AuthorizationPage):
        with pytest.raises((AssertionError, AuthorizationError)):  # noqa:
            main_page = authorization_page.authorize(username=username, password=password)
            main_page.check_url_negative()


class TestMainPage:
    """Tests for main page"""

    @pytest.fixture(scope="function")
    def main_page(self, registration_page: RegistrationPage):
        username, email, password = make.auth_data()
        return registration_page.pass_registration(username=username, email=email,
                                                   password=password)

    @pytest.mark.UI
    def test_unauthorized_access(self, main_page: MainPage):
        session = main_page.session_cookie
        assert session is not None
        char = session[5].swapcase() if session[5].isascii() else 'X'
        session = session[:5] + char + session[6:]
        response = requests.get(change_netloc(main_page.current_url,
                                              main_page.settings.app_api_netloc),
                                cookies={'session': session},
                                headers={'User-Agent': main_page.user_agent}, timeout=1,
                                allow_redirects=False)
        check.not_equal(response.status_code, 200)

    @pytest.mark.UI
    def test_citations(self, main_page: MainPage):
        for _ in range(25):
            check.is_in(main_page.wisdom_citation, wisdom_citations)
            main_page.refresh()

    @pytest.mark.UI
    @pytest.mark.parametrize('vk_id', ['0', '<script>alert(1);</script>', 'some-vk-id'])
    def test_vk_id(self, vk_id, main_page: MainPage, mock_client: MockClient):
        username = main_page.username
        mock_client.set_vk_id(username, vk_id)
        main_page.refresh()
        try:
            check.equal(main_page.vk_id, vk_id)
        except WebDriverException as err:
            raise AssertionError('vk_id element not found') from err

    @allure.step('Check all links on the page')
    @pytest.mark.UI
    @pytest.mark.enable_video
    def test_other_page_urls(self, main_page: MainPage, settings: Settings):
        @allure.step('Check link on the page')
        def check_url1(locator, error_msg=''):
            html = main_page.find((By.TAG_NAME, 'html'))
            handle = driver.current_window_handle
            try:
                main_page.click(locator)
                main_page.wait(settings.time_load_page).until(conditions.staleness_of(html))
            except WebDriverException:
                main_page.make_request()
                raise AssertionError(error_msg)
            if handle == driver.current_window_handle:
                main_page.make_request()
            else:
                driver.close()
                driver.switch_to.window(handle)

        @allure.step('Check link on the page')
        def check_url2(pair, error_msg=''):
            html = main_page.find((By.TAG_NAME, 'html'))
            handle = driver.current_window_handle
            try:
                locator1 = pair[0]
                locator2 = pair[1]
                ActionChains(driver) \
                    .move_to_element(driver.find_element(locator1)) \
                    .pause(1) \
                    .click(driver.find_element(locator2)) \
                    .perform()
                main_page.wait(settings.time_load_page).until(conditions.staleness_of(html))
            except WebDriverException:
                if handle == driver.current_window_handle:
                    main_page.make_request()
                else:
                    driver.close()
                    driver.switch_to.window(handle)
                raise AssertionError(error_msg)
            main_page.make_request()

        driver = main_page.driver
        link_locators = main_page.locators
        with check.check:
            check_url1(link_locators.API, 'invalid url for API link')
        with check.check:
            check_url1(link_locators.FUTURE, 'invalid url for future internet link')
        with check.check:
            check_url1(link_locators.SMTP, 'invalid url for SMTP link')
        with check.check:
            check_url1(link_locators.PYTHON, 'invalid url for python link')
        with check.check:
            check_url1(link_locators.LINUX, 'invalid url for linux link')
        with check.check:
            check_url1(link_locators.NETWORK, 'invalid url for network link')
        with check.check:
            check_url2([link_locators.PYTHON, link_locators.PYTHON_HISTORY],
                       'invalid url for python history link')
        with check.check:
            check_url2([link_locators.PYTHON, link_locators.FLASK],
                       'invalid url for flask link')
        with check.check:
            check_url2([link_locators.LINUX, link_locators.CENTOS],
                       'invalid url for centos link')
        with check.check:
            check_url2([link_locators.NETWORK, link_locators.WIRESHARK_NEWS],
                       'invalid url for wireshark news link')
        with check.check:
            check_url2([link_locators.NETWORK, link_locators.WIRESHARK_DOWNLOAD],
                       'invalid url for wireshark download link')
        with check.check:
            check_url2([link_locators.NETWORK, link_locators.TCPDUMP_EXAMPLES],
                       'invalid url for tcpdump examples link')
