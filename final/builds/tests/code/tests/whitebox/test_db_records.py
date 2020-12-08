import time

import allure
import pytest

from clients.mysql_client import MysqlClient
from clients.api_client import ApiClient
from mysql_utils.record import Record
from ui.pages.authorization_page import AuthorizationPage, AuthorizationError
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from utils import make


class TestApi:
    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('x' * 100, 'email@my.email', 'password', id='long username'),
        pytest.param('ussrname', 'email' * 100 + '@liam.ru', 'mypass', id='long email'),
        pytest.param('u53rNaM3', 'Imail@III.ru', 'F' * 1000, id='long password'),
        pytest.param('s', 'em@email.org', 'mypassword', id='short username'),
        pytest.param('s' * 8, 'm', 'p' * 12, id='short invalid email')
    ])
    def test_add_user_negative(self, username, email, password, mysql_client: MysqlClient,
                               api_client: ApiClient):
        """Test status code of API function 'add_user'

        Steps:
            Call 'add_user' with some credentials and check record with these credentials in the users' table

        Expected  results:
            Status code is 400 and record with these credentials no exists in the users' table
            or another status code and the record exists
        """
        response = api_client.add_user(username, email, password)
        record = mysql_client.get_record(username)
        assert response.status_code == 400 and record is None \
               or record == Record(username, email, password, 1, 0, None)


class TestScenarios:
    @allure.title("Scenario for single user (1)")
    @pytest.mark.scenario
    def test_scenario_single_user(self, api_client: ApiClient, mysql_client: MysqlClient,
                                  authorization_page: AuthorizationPage):
        """Test scenario for API

        Steps:
            0 Generate credentials
            1 Add user via API
            2 Delete user via API
            3 Add user via API
            4 Accept user via API
            5 Block user via API
            6 Accept user via API
            7 Authorize user via API
            8 Logout
            9 Block user via API
            0 Try to authorize user
        Expected results:
            Step 1: database table has record with these credentials and values `access` = 1,
              `active` = 0, `start_active_time` = None
            Step 2: record does not exist for this username
            Steps 3-4: database table has record with these credentials and values `access` = 1,
              `active` = 0, `start_active_time` = None
            Step 5: `access` = 0, no other changes
            Step 6: `access` = 1, no other changes
            Step 7: User succeeds to authorize, `active` changed to 1, start_active_time changed
            and almost equal time.time(), no other changes
            Step 8: `active` = 0, no other changes
            Step 9: `access` = 0, no other changes
            Step 10: User doesn't succeed to authorize, the record doesn't changed
        """
        username, email, password = make.auth_data()
        with allure.step('Add user'):
            api_client.add_user(username=username, email=email, password=password)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)
        with allure.step('Del user'):
            api_client.del_user(username=username)
            assert mysql_client.get_record(username) is None  # record not exists
        with allure.step('Add user'):
            api_client.add_user(username=username, email=email, password=password)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)
        with allure.step('Accept user'):
            api_client.accept_user(username=username)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)  # no changes
        with allure.step('Block user'):
            api_client.block_user(username=username)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 0, 0, None)  # access = 0
        with allure.step('Accept user'):
            api_client.accept_user(username=username)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 1, 0, None)
        with allure.step('Authorize user'):
            main_page = authorization_page.authorize(username, password)
            record = mysql_client.get_record(username)
            start_time = time.time()
            assert record is not None
            assert record == Record(username, email, password, 1, 1, start_time)  # active = 1
        with allure.step('Logout'):
            main_page.logout()
            assert record is not None
            assert record == Record(username, email, password, 1, 0, start_time)  # active = 0
        with allure.step('Block user'):
            api_client.block_user(username=username)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # access = 0
        with allure.step('Authorize user (who is blocked)'):
            with pytest.raises(AuthorizationError):
                authorization_page.authorize(username, password)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # no changes

    @allure.title("Scenario for single user (2)")
    @pytest.mark.scenario
    def test_scenario_single_user_2(self, api_client: ApiClient, mysql_client: MysqlClient,
                                    registration_page: RegistrationPage):
        """Test scenario for API

                Steps:
                    0 Generate credentials
                    1 Pass registration with these credentials
                    2 Block user via API
                    3 Refresh page
                    4 Try to authorize to the site
                    5 Accept user via API
                    6 Try to authorize user
                Expected results:
                    Step 1: database table has record with these credentials and values `access` = 1,
                      `active` = 1, `start_active_time` ~ time.time()
                    Step 2: `access` = 0, no other changes
                    Step 3: user is redirected to authorization page, `access` = 0, `active` = 0
                    Step 4: user doesn't succeed to authorize,
                    Step 6: `access` = 1, no other changes
                    Step 7: User succeeds to authorize, `active` changed to 1, start_active_time changed
                    and almost equal time.time(), no other changes
                    Step 8: `active` = 0, no other changes
                    Step 9: `access` = 0, no other changes
                    Step 10: User doesn't succeed to authorize, the record doesn't changed
                """
        username, email, password = make.auth_data()
        with allure.step('Register user'):
            main_page = registration_page.pass_registration(username, email, password)
            start_time = time.time()
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 1, 1, start_time)  # access = 1, active = 1
        with allure.step('Block user'):
            api_client.block_user(username=username)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # access = 0, active = 0
        with allure.step('Refresh page'):
            main_page.refresh()
            assert not MainPage.is_opened(main_page.driver)
            assert AuthorizationPage.is_opened(main_page.driver)  # logout
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # no change
        authorization_page = AuthorizationPage(main_page.driver, main_page.settings)
        with allure.step('Authorize user (who is blocked)'):
            with pytest.raises(AuthorizationError):
                authorization_page.authorize(username, password)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 0, 0, start_time)  # no change
        with allure.step('Accept user'):
            api_client.block_user(username=username)
            record = mysql_client.get_record(username)
            assert record is not None
            assert record == Record(username, email, password, 1, 0, start_time)  # access = 1
        with allure.step('Authorize user (who was accepted)'):
            authorization_page.authorize(username, password)
            record = mysql_client.get_record(username)
            start_time = time.time()
            assert record is not None
            assert record == Record(username, email, password, 1, 1, start_time)  # active = 1
