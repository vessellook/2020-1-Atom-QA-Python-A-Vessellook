"""Tests for WEB interface of myapp"""
import time

import allure
import pytest
# Functions in this package works as operator assert but not stop execution
import pytest_check as check
from selenium.common.exceptions import WebDriverException
import requests

from utils.citations import wisdom_citations
from utils.common import change_netloc
from ui.pages.registration_page import RegistrationPage, RegistrationError
from ui.pages.authorization_page import AuthorizationPage, AuthorizationError
from ui.pages.main_page import MainPage
from clients.mock_client import MockClient
from utils import make


class TestRegistrationPage:
    """Tests for validation of registration page"""

    @pytest.mark.UI
    @pytest.mark.smoke
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('validusername', 'validemail@mail.ru', 'validpassword',
                     id='Normal case (1)'),
        pytest.param('usernamevalid', 'validemail@corp.mail.ru', 'validpassword',
                     id='Normal case (2)'),
        pytest.param('1mv41idt00', 'it1sv41idt00@gmail.com', 'validpassword',
                     id='Normal case (3)'),
    ])
    def test_valid_credentials(self, username, email, password,
                               registration_page: RegistrationPage):
        """Test registration with valid credentials

        Steps:
            - Open registration page and try to pass registration
        Expected results:
            Current page url path contains 'welcome', so the current page is main
        """
        try:
            main_page = registration_page.pass_registration(username=username, email=email,
                                                            password=password)
        except RegistrationError as err:
            raise AssertionError from err
        main_page.check_url()

    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'email', 'password', 'confirm_password'], [
        pytest.param('validuser1', 'validemail1@email.valid', '', '', marks=pytest.mark.smoke,
                     id="empty password"),
        pytest.param("validuser2", '', 'validpassword', None, marks=pytest.mark.smoke,
                     id="empty email"),
        pytest.param("", "validemail3@email.valid", 'validpassword', None,
                     marks=pytest.mark.smoke, id="empty username"),
        pytest.param('validuser4', 'invalidemail@', 'validpassword', None,
                     id="email without domain"),
        pytest.param('validuser5', "@email.invalid", 'validpassword', None,
                     id="email without login"),
        pytest.param("validuser6", 'email.invalid', 'validpassword', None,
                     id="email without login@"),
        pytest.param("validuser7", "invalidemail7@.ru", 'validpassword', None,
                     id="email with invalid domain"),
        pytest.param("validuser8", "invalidemail8@mail.", "validpassword", None,
                     id="invalid email domain"),
        pytest.param("validuser9", "invalidemail9", "validpassword", None,
                     id="invalid email (1)"),
        pytest.param("validuser10", "invalidemail", "validpassword", None,
                     id="invalid email (2)"),
        pytest.param("validuser11", "invalidemail11@email.74", "validpassword", None,
                     id="numeric email"),
        pytest.param("validuser12", "validemail@email.valid", "validpassword", '',
                     marks=pytest.mark.smoke,
                     id="empty confirm_password field"),
        pytest.param("validuser13", "validemail@email.valid", "validpassword", "notequal",
                     marks=pytest.mark.smoke,
                     id="confirm_password field and password are different")])
    def test_invalid_credentials(self, username, email, password, confirm_password,
                                 registration_page: RegistrationPage):
        """Test registration with invalid credentials

        Steps:
            - Open registration page and try to pass registration
        Expected results:
            Current page url path doesn't contain 'welcome', so the current page is main
        """
        with pytest.raises(RegistrationError):
            registration_page.pass_registration(username=username, email=email,
                                                password=password,
                                                confirm_password=confirm_password)

    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('u', 'some@some.email', 'somepassword', id='short but not empty username'),
        pytest.param('u' * 5, 'mem@some.email', 'somepassword', id="5 letters' username"),
        pytest.param('u' * 6, 'eme@some.email', 'somepassword', id="6 letters' username"),
        pytest.param('u' * 16, 'em@some.email', 'somepassword', id="16 letters' username"),
        pytest.param('u' * 17, 'emo@some.email', 'somepassword', id="17 letters' username"),
        pytest.param('u' * 100, 'long@some.email', 'somepassword', id="long' username"),
        pytest.param('userwithname', 'e', 'somepassword', id='short but not empty invalid email'),
        pytest.param('userrrname', 'a@b.c', 'somepassword', id='short but not empty valid email'),
        pytest.param('u' * 10, ('long' * 100 + '@some.email')[-64:], 'somepassword',
                     id="64 letters' email"),
        pytest.param('u' * 11, ('long' * 100 + '@some.email')[-65:], 'somepassword',
                     id="65 letters' email"),
        pytest.param('u' * 12, 'long' * 100 + '@some.email', 'somepassword', id="long email"),
        pytest.param('u' * 9, 'longlo@some.email3', 's' * 10, id="email with digit at the end"),
        pytest.param('u' * 15, 'short@some.email', 's', id='short but not empty password'),
        pytest.param('u' * 13, 'longer@some.email', 's' * 255, id="255 letters' password"),
        pytest.param('u' * 14, 'longlong@some.email', 's' * 256, id="256 letters' password"),
        pytest.param('u' * 8, 'longest@some.email', 's' * 1000, id="long password"),
        pytest.param('u' * 8 + '_', 'under@some.email', 's' * 9, id="underscore"),
        pytest.param('u' * 8 + '-', 'hyphen@some.email', 's' * 9, id="hyphen"),
    ])
    def test_integrity(self, username, email, password, registration_page: RegistrationPage):
        """Test integrity of registration and authorization"""
        try:
            main_page = registration_page.pass_registration(username=username, email=email,
                                                            password=password)
        except RegistrationError:
            with allure.step('Registration not succeed. Check that authorization will not succeed'):
                authorization_page = AuthorizationPage(registration_page.driver,
                                                       registration_page.settings)
                authorization_page.make_request()  # open authorization page
                with pytest.raises(AuthorizationError):
                    authorization_page.authorize(username=username, password=password)
        else:
            with allure.step('Registration succeed. Check that authorization will succeed'):
                authorization_page = main_page.logout()
                try:
                    authorization_page.authorize(username=username, password=password)
                except AuthorizationError as err:
                    allure.attach.file(
                        authorization_page.make_screenshot('not_succeed_authorization'),
                        attachment_type=allure.attachment_type.PNG,
                        name='not_succeed_authorization.png')
                    raise AssertionError from err  # to mark test as failed, not broken


class TestAuthorizationPage:
    """Tests for authorization page"""

    @pytest.mark.UI
    @pytest.mark.enable_video
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('wk33NtzvQHW3kHMs', 'U3Aje@Kr0poHTbe.0rFu', 'XkJWFH98GhJgvNdg')
    ])
    def test_authorization_positive(self, username, email, password,
                                    registration_page: RegistrationPage):
        """Test authorization after registration"""
        main_page = registration_page.pass_registration(username=username, email=email,
                                                        password=password)
        authorization_page = main_page.logout()
        authorization_page.authorize(username=username, password=password)
        allure.attach.file(main_page.make_screenshot('test_authorization_positive'),
                           attachment_type=allure.attachment_type.PNG)
        main_page.check_url()

    @pytest.mark.UI
    @pytest.mark.parametrize(['username', 'password'], [
        ('iwanttoenter', 'iwanttoenterpass'),
        pytest.param('mycoolusername', '', id='empty password'),
        pytest.param('', 'mycoolpassword', id='empty username'),
    ])
    def test_authorization_negative(self, username, password,
                                    authorization_page: AuthorizationPage):
        """Test authorization without registration"""
        with pytest.raises(AuthorizationError):  # noqa:
            authorization_page.authorize(username=username, password=password)


class TestMainPage:
    """Tests for main page"""

    @pytest.fixture(scope="function")
    def main_page(self, registration_page: RegistrationPage):
        """Fixture-helper to open main page of new user"""
        username, email, password = make.auth_data()
        return registration_page.pass_registration(username=username, email=email,
                                                   password=password)

    @pytest.mark.UI
    def test_wrong_session(self, main_page: MainPage):
        """Test that user can't access main page if user's session cookie is wrong"""
        session = main_page.session_cookie
        assert session is not None
        session = session[:-1] + 'X' if session[-1] != 'X' else 'Y'
        response = requests.get(change_netloc(main_page.current_url,
                                              main_page.settings.app_api_netloc),
                                cookies={'session': session},
                                headers={'User-Agent': main_page.user_agent},
                                timeout=1,
                                allow_redirects=False)
        assert response.status_code != 200

    @pytest.mark.UI
    def test_citations(self, main_page: MainPage):
        """Test that citations in the footer are correct"""
        for _ in range(25):
            citation = main_page.wisdom_citation
            with check.check, allure.step(f"Check '{citation}'"):
                assert main_page.wisdom_citation in wisdom_citations
            main_page.refresh()

    @pytest.mark.UI
    @pytest.mark.enable_video
    @pytest.mark.parametrize('vk_id', ['0', '<script>alert(1);</script>', 'some-vk-id'])
    def test_vk_id(self, vk_id, main_page: MainPage, mock_client: MockClient):
        """Test that vk_id is displayed correctly if it has correct string value"""
        username = main_page.username
        mock_client.set_vk_id(username, vk_id)
        time.sleep(2)
        main_page.refresh()
        with allure.step('search for vk_id'):
            try:
                real_vk_id = main_page.vk_id
            except WebDriverException as err:
                allure.attach.file(main_page.make_screenshot('vk_id'),
                                   attachment_type=allure.attachment_type.PNG,
                                   name='vk_id--not--found.png')
                raise AssertionError('vk_id element not found') from err
        with allure.step('Compare expected and real vk_id'):
            check.equal(real_vk_id, vk_id)
