"""Tests for myapp API functions, that only compare expected and real status codes"""
import allure
import pytest
import requests
# This function works as operator assert but not stop execution
import pytest_check as check
from selenium.common.exceptions import WebDriverException

from clients.api_client import ApiClient
from ui.pages.authorization_page import AuthorizationPage, AuthorizationError
from utils import status_codes, make
from utils.common import attach_http


def test_status(api_client: ApiClient):
    """Test that get_status API function works well

    Steps:
        - Make request to application with path '/status'

    Expected results:
        Response status code is 200
        Response header 'Content-Type' has value 'application/json'
        Response body is valid JSON that has field 'status' wit value 'ok'
    """
    response = api_client.get_status()
    check.equal(response.status_code, status_codes.OK)
    check.equal(response.headers['Content-Type'], 'application/json')
    check.equal(response.json()['status'], 'ok')


class TestAdd:
    """Tests for add_user API function"""

    @pytest.mark.API
    @pytest.mark.smoke
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("uZ5iwv9mHRau2XwUyq", "O0pUmj65FwBK5@BEX4B0Ic304jp.Jn_X",
                     "_nPnV9OXAUv4BRd8u4x",
                     id="status code 210 instead of 201 [1]"),
        pytest.param("lgsI2JTTROPy", "ufA0AAb93mU@GgKg5eAlDqAF7y.jVdX", "c1oGe2lpHykxh",
                     id="status code 210 instead of 201 [2]"),
        pytest.param("SxXkQphZlyU", "Nt_2EANGatP@corp.mail.ru", "k7p4abS9pz8",
                     id="status code 210 instead of 201 [3]"),
    ])
    def test_valid_credentials(self, username, email, password,
                               api_client: ApiClient):
        """Test add_user API function with valid credentials

        Steps:
            - Make request to application with path /api/add_user. JSON in valid format like
            {"username": "someusername", "email": "some@email.ru", "password": "somepassword"}
        Expected results:
            Response status code is 201
        """
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == 201

    @pytest.mark.API
    @pytest.mark.smoke
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('uservalid1', 'emailvalid1@email.valid', '', marks=pytest.mark.smoke,
                     id="empty password"),
        pytest.param("uservalid2", '', 'validpassword', marks=pytest.mark.smoke,
                     id="empty email"),
        pytest.param("", "emailvalid3@email.valid", 'validpassword', marks=pytest.mark.smoke,
                     id="empty username"),
        pytest.param('uservalid4', 'emailinvalid@', 'validpassword',
                     id="email without domain"),
        pytest.param('uservalid5', "@invalid.email", 'validpassword',
                     id="email without login"),
        pytest.param("uservalid6", 'invalid.email', 'validpassword',
                     id="email without login@"),
        pytest.param("uservalid7", "emailinvalid7@.ru", 'validpassword',
                     id="email with invalid domain"),
        pytest.param("uservalid8", "emailinvalid8@mail.", "validpassord",
                     id="invalid email domain"),
        pytest.param("uservalid9", "emailinvalid9", "validpassword", id="invalid email (1)"),
        pytest.param("uservalid10", "emailinvalid", "validpassword", id="invalid email (2)"),
        pytest.param("uservalid11", "emailinvalid11@email.74", "validpassword", id="numeric email"),
    ])
    def test_invalid_credentials(self, username, email, password, api_client: ApiClient):
        """Test add_user API function with invalid credentials

        Steps:
            - Make request to application with path /api/add_user. JSON in valid format like
            {"username": "someusername", "email": "some@email.ru", "password": "somepassword"}
        Expected results:
            Response status code is 400
        """
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == 400

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param('n', 'some@any.email', 'somepassword', id='short but not empty username'),
        pytest.param('n' * 5, 'mem@any.email', 'somepassword', id="5 letters' username"),
        pytest.param('n' * 6, 'eme@any.email', 'somepassword', id="6 letters' username"),
        pytest.param('n' * 16, 'em@any.email', 'somepassword', id="16 letters' username"),
        pytest.param('n' * 17, 'emo@any.email', 'somepassword', id="17 letters' username"),
        pytest.param('n' * 100, 'long@any.email', 'somepassword', id="long' username"),
        pytest.param('nameofuser', 'f', 'somepassword', id='short but not empty invalid email'),
        pytest.param('usernnname', 'd@b.c', 'somepassword', id='short but not empty valid email'),
        pytest.param('n' * 10, ('long' * 100 + '@any.email')[-64:], 'somepassword',
                     id="64 letters' email"),
        pytest.param('n' * 11, ('long' * 100 + '@any.email')[-65:], 'somepassword',
                     id="65 letters' email"),
        pytest.param('n' * 12, 'long' * 100 + '@any.email', 'somepassword', id="long email"),
        pytest.param('n' * 9, 'longlo@any.email3', 's' * 10, id="email with digit at the end"),
        pytest.param('u' * 15, 'short@any.email', 's', id='short but not empty password'),
        pytest.param('n' * 13, 'longer@any.email', 's' * 255, id="255 letters' password"),
        pytest.param('n' * 14, 'longlong@any.email', 's' * 256, id="256 letters' password"),
        pytest.param('n' * 8, 'longest@any.email', 's' * 1000, id="long password"),
        pytest.param('n' * 8 + '_', 'under@any.email', 's' * 9, id="underscore"),
        pytest.param('n' * 8 + '-', 'hyphen@any.email', 's' * 9, id="hyphen"),
    ])
    def test_integrity(self, username, email, password, authorization_page: AuthorizationPage,
                       api_client: ApiClient):
        """Test integrity of add_user API function and authorization

        Steps:
            - Make request to application with path /api/add_user and JSON in valid format like
            {"username": "someusername", "email": "some@email.ru", "password": "somepassword"}
            - Try to authorize to the site with the same credentials

        Expected results:
            If request to /api/add_user has status code 400 or more,
            user mustn't be able to authorize to the site with these credentials
            In other cases user must be able to authorize to the site with these credentials
        """
        response = api_client.add_user(username=username, email=email, password=password)
        if response.status_code >= 400:
            with allure.step("'add_user' not succeed. Check that authorization will not succeed"):
                with pytest.raises(AuthorizationError):
                    authorization_page.authorize(username=username, password=password)
        else:
            with allure.step("'add_user' succeed. Check that authorization will succeed"):
                try:
                    authorization_page.authorize(username=username, password=password)
                except AuthorizationError as err:
                    allure.attach.file(
                        authorization_page.make_screenshot('not_succeed_authorization'),
                        attachment_type=allure.attachment_type.PNG,
                        name='not_succeed_authorization.png')
                    raise AssertionError from err  # to mark test as failed, not broken

    @pytest.mark.API
    @pytest.mark.parametrize('json', [
        {},
        [],
        {'username': 'JmJ46wL1CgObdlYZfY'},
        {'email': 'CcO2hP0pccOTDGyBOi@O56LMJgwOyrtO.wzGz'},
        {'password': 'SlyVs9BNtXVcd3NyC'},
        {'username': 'B2kthWKJSZa2m',
         'email': 'R8VfWkQncDCg4CzTElp3@sSZcFnRcm7uyoiwcE3z.ltFu9'},
        {'username': 'AKsgVG9GXPcvxPQOzkDH', 'password': 'iFoe4A65FZ1'},
        {'email': 'nHsv74vKecBib0Zfz@7GLvNEU4xAQ.dPNsf',
         'password': 'vUCyRJ6W70Q9EoADN_'},
        pytest.param({'username': -5, 'password': False, 'email': []},
                     id='210 status code instead of 400'),
        ['not', 'empty', 'list'],
        {'not': 'empty', 'dictionary': True},
        'just string'])
    def test_invalid_json(self, json, api_client: ApiClient):
        """Test status codes for requests with different invalid JSON

        Steps:
            - Make request to application with path /api/add_user and JSON in invalid formats

        Expected results:
            Response status code is 400
        """
        with allure.step('Send invalid json to add user'):
            response = requests.post(f'http://{api_client.netloc}/api/add_user',
                                     cookies=api_client.cookies,
                                     headers=api_client.headers,
                                     json=json)
            attach_http(response)
            assert response.status_code == 400

    @pytest.mark.API
    @pytest.mark.smoke
    def test_authorize_after_add(self, authorization_page: AuthorizationPage,
                                 api_client: ApiClient):
        """Test that user, created by API, can authorize properly

        Steps:
            - Make request to application with path /api/add_user and JSON in valid format
            - Try to authorize with the same credentials

        Expected results:
            Response status code is 200 for API request
            User succeed to authorize
        """
        username, email, password = make.auth_data()
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code in range(200, 300)
        try:
            authorization_page.authorize(username=username, password=password)
        except WebDriverException as err:
            raise AssertionError from err

    @pytest.mark.API
    def test_add_two_users_with_same_email(self, api_client: ApiClient):
        """Test that it is impossible to create two users with same email

        Steps:
            - Make request to application with path /api/add_user and JSON in valid format
            - Make another request to application with path /api/add_user
              but different username and password
        Expected results:
            Status code for the first request is in 200-300 range
            Status code for the first request is in 400-500 range
        """
        username, email, password = make.auth_data()
        username2, _, password2 = make.auth_data(email=email)
        with allure.step('Add the first user and check status code is in range 200 to 300'):
            response = api_client.add_user(username=username, email=email, password=password)
            attach_http(response, '1')
            assert response.status_code in range(200, 300)
        with allure.step('Add the second user and check status code is in range 400 to 500'):
            response2 = api_client.add_user(username=username2, email=email, password=password2)
            attach_http(response2, '2')
            assert response2.status_code in range(400, 500)


class TestDel:
    """Tests for del_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("jXlBnTbc5gpiz9iMy", "ye2YVs9cHG45@tKYxoKA_8VlwZxA.Cd0D1", "ooNkWYnmo5qFF_"),
        pytest.param("FiAkvDxsjCx", "UdXeLmsauBY3@UZw9bEbYbZPSldSoS.0qw5S", "9Yl4hp5_Zn4KQHE7D"),
        pytest.param("DAPKr0XEW1", "4F6Dbz7uaxnK@corp.mail.ru", "RKpZTwTMoXXCyNMl"),
        pytest.param("bWRp_WCZekujTS", "h3rqt_Zt8eld1@IhNo17B0f7U6p.QI_",
                     "bIKc98EZCZjqCBDBJ1v0' or 1 = 1 '; DROP DATABASE; --",
                     id="sql injection in password"),
    ])
    def test_added_users(self, username, email, password, api_client: ApiClient):
        """Test that users deleted


        Steps:
            - Make request to application with path /api/add_user and JSON in valid format
            - Make request to application with path /api/del_user/<username>
            - Make request to application with path /api/del_user/<username> again

        Expected results:
            Status code for the first request is in 200-300 range
            Status code for the second request is 204
            Status code for the third request is 404
        """
        response = api_client.add_user(username=username, email=email, password=password)
        attach_http(response, '1')
        if response.status_code not in range(200, 300):
            raise Exception('there was error with add_user function')
        with allure.step('Del user'):
            response2 = api_client.del_user(username)
            attach_http(response2, '2')
            assert response2.status_code == status_codes.DELETED
        with allure.step('Del user again'):
            response3 = api_client.del_user(username)
            attach_http(response3, '3')
            assert response3.status_code == status_codes.NOT_EXIST


class TestBlock:
    """Tests for block_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("oleVPFC4MrSJ5M2a4ty", "qtfmQG0TlMdqlZi2@ffsLCGnpVdH.3K0p", "Wf8bAkMOEPBngn"),
        pytest.param("2URYaA7ebE", "64AIR1LVJjJ_CEpbIR@YnUbudscDZzHQ.qx_wK", "S83adQxS6jGltbzR0w"),
        pytest.param("PLKapvmJTRpKerTsh", "PCzaRwYlMitt8@corp.mail.ru", "40GJGhVClBLO69DctqQ"),
        pytest.param("AnRY07pepWosuWi9", "IH1Jsht9U6e60MJpNNs@czwPpmi0HNHzPETQ.0vQj1",
                     "yQMmMzi6MAjLN' or 1 = 1 '; DROP DATABASE; --",
                     id="sql injection in password"),
    ])
    def test_added_users(self, username, email, password, api_client: ApiClient):
        """Tests that users blocked

        Steps:
            - Make request to application with path /api/add_user and JSON in valid format
            - Make request to application with path /api/block_user/<username>
            - Make request to application with path /api/block_user/<username> again

        Expected results:
            Status code for the first request is in 200-300 range
            Status code for the second request is 200
            Status code for the third request is 304
        """
        response = api_client.add_user(username=username, email=email, password=password)
        attach_http(response, '1')
        if response.status_code not in range(200, 300):
            raise Exception('there was error with add_user function')
        with allure.step('Block user'):
            response2 = api_client.block_user(username)
            attach_http(response2, '2')
            assert response2.status_code == status_codes.OK
        with allure.step('Block user again'):
            response3 = api_client.block_user(username)
            attach_http(response3, '3')
            assert response3.status_code == status_codes.NOT_CHANGED


class TestAccept:
    """Tests for accept_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("W5bezo0pLs", "fH899uQfEQ6Gm6w@vmQJERazZPaT7yIprOVr.dUu", "3dFu4irYDL"),
        pytest.param("R_4uFz3zDYO2Y", "fq69Dfjhw9MJXfc@FpGgyxUfKqd.b6Nv", "wnCf0CvS1oibfY_N"),
        pytest.param("lM_9nXk6FC8eCDdu", "oS8sXS3iQDWB7lQf@corp.mail.ru", "in4NMj2A_OFxMkA"),
        pytest.param("sHctkbP27IiZFR", "c0bmefgdcajxiL22kD_@yS_jK_k0ZoX5K7r.wNtP",
                     "tXJL1_dD60TvUUC_6ksp' or 1 = 1 '; DROP DATABASE; --",
                     id="sql injection in password")
    ])
    def test_added_users(self, username, email, password, api_client: ApiClient):
        """Tests accept_user API function for users

        Steps:
            - Make request to application with path /api/add_user and JSON in valid format
            - Make request to application with path /api/accept_user/<username>
            - Make request to application with path /api/block_user/<username>
            - Make request to application with path /api/accept_user/<username>
            - Make request to application with path /api/accept_user/<username>

        Expected results:
            Status code for the first request is in 200-300 range
            Status code for the second request is 304
            Status code for the fourth request is 200
            Status code for the fifth request is 304
        """
        response = api_client.add_user(username=username, email=email, password=password)
        attach_http(response, '1')
        if response.status_code not in range(200, 300):
            raise Exception('there was error with add_user function')
        with allure.step("Accept user that wasn't blocked"):
            response2 = api_client.accept_user(username)
            attach_http(response2, '2')
            assert response2.status_code == status_codes.NOT_CHANGED
        with allure.step('Block user and accept him'):
            response3 = api_client.block_user(username)
            attach_http(response3, '3')
            response4 = api_client.accept_user(username)
            attach_http(response4, '4')
            assert response4.status_code == status_codes.OK
        with allure.step('Accept user again'):
            response5 = api_client.accept_user(username)
            attach_http(response5, '5')
            assert response5.status_code == status_codes.NOT_CHANGED
