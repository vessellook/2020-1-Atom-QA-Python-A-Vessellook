from urllib.parse import urljoin

import allure
import pytest
import pytest_check as check
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions

from ui.pages.authorization_page import AuthorizationPage
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from utils import make
from utils.common import change_netloc, attach_http


@pytest.fixture(scope="function")
def main_page(registration_page: RegistrationPage):
    username, email, password = make.auth_data()
    return registration_page.pass_registration(username=username, email=email,
                                               password=password)


@allure.step('Check link on the page')
def check_link(main_page: MainPage, locator, error_msg=''):
    html = main_page.find((By.TAG_NAME, 'html'))
    try:
        main_page.click(locator)
        main_page.wait(main_page.load_time).until(conditions.staleness_of(html))
    except WebDriverException as err:
        raise AssertionError(error_msg) from err
    assert main_page.check_url_negative()


@allure.step('Check nested link on the page')
def check_nested_link(main_page: MainPage, parent_locator, nested_locator, error_msg=''):
    html = main_page.find((By.TAG_NAME, 'html'))
    driver = main_page.driver
    try:
        ActionChains(driver) \
            .move_to_element(driver.find_element(parent_locator)) \
            .pause(1) \
            .click(driver.find_element(nested_locator)) \
            .perform()
        main_page.wait(main_page.load_time).until(conditions.staleness_of(html))
    except WebDriverException as err:
        raise AssertionError(error_msg) from err
    assert main_page.check_url_negative()


def check_links(main_page: MainPage, params: tuple):
    driver = main_page.driver
    for locator, label in params:
        handle = driver.current_window_handle
        with check.check:
            check_link(main_page, locator, f'invalid url for {label} link')
        if handle == driver.current_window_handle:
            main_page.make_request()
        else:
            driver.close()
            driver.switch_to.window(handle)


def check_nested_links(main_page: MainPage, params: tuple):
    driver = main_page.driver
    for parent_locator, locator, label in params:
        handle = driver.current_window_handle
        with check.check:
            check_nested_link(main_page, parent_locator, locator, f'invalid url for {label} link')
        if handle == driver.current_window_handle:
            main_page.make_request()
        else:
            driver.close()
            driver.switch_to.window(handle)


@allure.title('Check all links on the page')
@pytest.mark.UI
@pytest.mark.enable_video
def test_main_page_links(main_page: MainPage):
    """Test links of main page have valid urls

    Steps:
        - Pass registration and enter main page (in fixture)
        - Click a link
        - Return to main page
        - Repeat for each links expect 'HOME'

    Expected results:
        All urls follow to some pages but not to main page
    """
    allure.attach.file(main_page.make_screenshot('main-page'),
                       attachment_type=allure.attachment_type.PNG,
                       name='main-page.png')
    link_locators = main_page.locators
    check_links(main_page, (
        (link_locators.API, 'API'),
        (link_locators.FUTURE, 'future'),
        (link_locators.SMTP, 'SMTP'),
        (link_locators.PYTHON, 'Python'),
        (link_locators.LINUX, 'Linux'),
        (link_locators.NETWORK, 'network')))
    check_nested_links(main_page, (
        (link_locators.PYTHON, link_locators.PYTHON_HISTORY, 'history'),
        (link_locators.PYTHON, link_locators.FLASK, 'Flask'),
        (link_locators.LINUX, link_locators.CENTOS, 'CentOS'),
        (link_locators.NETWORK, link_locators.WIRESHARK_NEWS, 'WireShark news'),
        (link_locators.NETWORK, link_locators.WIRESHARK_DOWNLOAD, 'WireShark downloads'),
        (link_locators.NETWORK, link_locators.TCPDUMP_EXAMPLES, 'TcpDump examples')))


@pytest.mark.UI
def test_source_links(authorization_page: AuthorizationPage):
    """Test all pages' sources exist

    Steps:
        - Open authorization page and collect all links to sources
        - Check sources one by one
        - Open registration page and collect all links to sources
        - Check sources one by one
        - Pass registration and enter main page, collect all links to sources
        - Check sources one by one

    Expected results:
        Each source response status code is 200

    Note: pytest_check functions can't be used inside function decorated by allure.step()
    because of allure.step() design. So allure report show status for each source,
    but pytest summary show only FAILURE for registration, authorization and main pages
    """
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


def get_urls_from_page(page: BasePage):
    """Collect urls to another pages and return absolute URLs"""
    html = BeautifulSoup(page.source, 'html.parser')
    urls = [a.get('href') for a in html.find_all('a')]
    return [url for url in urls if url is not None]


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
                attach_http(response, url)
                assert response.status_code == 200
        except AssertionError:
            all_right = False
    if not all_right:
        raise AssertionError(msg)
