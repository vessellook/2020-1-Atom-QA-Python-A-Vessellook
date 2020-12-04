import time

import allure
import pytest

from clients.mysql_client import MysqlClient
from mysql_utils.record import Record
from clients.api_client import ApiClient
from ui.pages.authorization_page import AuthorizationPage, AuthorizationError
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from utils import make


class TestApi:
    @allure.title('Check add_user API function')
    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        ('toollongusername0123456789012345678901234567890123456789012345678901234567890', 'email@my.email', 'password'),
        ('ussrname', 'email@tolongemail0212345890123456789012345678901234567890123456789012345678123mail.ru', 'mypass'),
        ('u53rNaM3', 'Imail@III.ru', 'tolongpass314159265358979323846264338327950288419716939937510582097494459230781'),
        ('u', 'em@email.org', 'mypassword'),
        ('uuuuuuuu', 'e', 'pppppppppppp')
    ])
    def test_add_user_negative(self, username, email, password, mysql_client: MysqlClient,
                               api_client: ApiClient):
        response = api_client.add_user(username, email, password)
        record = mysql_client.get_user(username).to_record()
        assert response.status_code == 400 \
               or record == Record(username, email, password, 1, 0, None)


class TestScenarios:
    @allure.title("Scenario for single user")
    @pytest.mark.scenario
    @pytest.mark.mixed
    def test_scenario_single_user(self, api_client: ApiClient, mysql_client: MysqlClient,
                                  authorization_page: AuthorizationPage):
        username, email, password = make.auth_data()
        with allure.step('Add user'):
            api_client.add_user(username=username, email=email, password=password)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)
        with allure.step('Del user'):
            api_client.del_user(username=username)
            assert mysql_client.get_user(username).to_record() is None  # record not exists
        with allure.step('Add user'):
            api_client.add_user(username=username, email=email, password=password)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)
        with allure.step('Accept user'):
            api_client.accept_user(username=username)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)  # no changes
        with allure.step('Block user'):
            api_client.block_user(username=username)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 0, 0, None)  # access = 0
        with allure.step('Accept user'):
            api_client.accept_user(username=username)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)
        with allure.step('Authorize user'):
            main_page = authorization_page.authorize(username, password)
            record = mysql_client.get_user(username).to_record()
            start_time = time.time()
            assert record is not None
            assert record == Record(username, email, password, 1, 1, start_time)  # active = 1
        with allure.step('Logout'):
            main_page.logout()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, start_time)  # active = 0
        with allure.step('Block user'):
            api_client.block_user(username=username)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # access = 0
        with allure.step('Authorize user (who is blocked)'):
            with pytest.raises(AuthorizationError):
                authorization_page.authorize(username, password)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # no changes

    @allure.title("Second scenario for single user")
    @pytest.mark.scenario
    @pytest.mark.mixed
    def test_scenario_single_user_2(self, api_client: ApiClient, mysql_client: MysqlClient,
                                    registration_page: RegistrationPage):
        username, email, password = make.auth_data()
        with allure.step('Register user'):
            main_page = registration_page.pass_registration(username, email, password)
            start_time = time.time()
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 1, 1, start_time)  # access = 1, active = 1
        with allure.step('Block user'):
            api_client.block_user(username=username)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # access = 1, active = 1
        with allure.step('Refresh page'):
            main_page.refresh()
            assert not MainPage.is_opened(main_page.driver)
            assert AuthorizationPage.is_opened(main_page.driver)  # logout
            authorization_page = AuthorizationPage(main_page.driver, main_page.settings)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # no change
        with allure.step('Authorize user (who is blocked)'):
            with pytest.raises(AuthorizationError):
                authorization_page.authorize(username, password)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # no change
        with allure.step('Accept user'):
            api_client.block_user(username=username)
            record = mysql_client.get_user(username).to_record()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, start_time)  # no change
        with allure.step('Authorize user (who was accepted)'):
            authorization_page.authorize(username, password)
            record = mysql_client.get_user(username).to_record()
            start_time = time.time()
            assert record is not None
            assert record == Record(username, email, password, 1, 1, start_time)  # active = 1
