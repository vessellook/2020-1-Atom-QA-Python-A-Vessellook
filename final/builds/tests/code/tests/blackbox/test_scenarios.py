"""Tests that contain many actions"""

from urllib.parse import urlparse

import allure
import pytest

from clients.api_client import ApiClient
from ui.pages.registration_page import RegistrationPage, RegistrationError
from ui.pages.authorization_page import AuthorizationError
from utils import make, status_codes
from utils.common import attach_http


@pytest.mark.scenario
def test_scenario1(registration_page: RegistrationPage, api_client: ApiClient):
    """Test how API functions influence user

    Steps:
        1 Pass registration with generated credentials
        2 Block user via block_user API function
        3 Refresh page
        4 Open registration page and try to register with the same credentials again
        5 Open authorization page and try to authorize to the site with the same credentials
        6 Accept user via accept_user API function
        7 Refresh page
        8 Delete user via del_user API function
        9 Refresh page
        0 Open authorization page and try to authorize to the site with the same credentials
        1 Open registration page and register with same credentials again
    Expected results:
        Steps 1-2 succeed
        Step 3 redirect to authrization page
        Steps 4-5 fail, pytest.raises catch Exception
        Step 6 succeed
        Step 7 redirect to main page
        Step 8 succeed
        Step 9 redirect to authorization page
        Step 10 fail, pytest.raises catch Exception
        Step 11 succeed
    """
    username, email, password = make.auth_data()
    with allure.step("Pass registration"):
        main_page = registration_page.pass_registration(username=username, password=password,
                                                        email=email)
        assert 'welcome' in urlparse(main_page.current_url).path
    with allure.step(f"Block user {username}"):
        response = api_client.block_user(username)
        attach_http(response)
    with allure.step("Refresh page"):
        main_page.refresh()
        assert 'welcome' not in urlparse(main_page.current_url).path
    with allure.step("Open registration page and try to register with same credentials again"):
        registration_page.make_request()
        with pytest.raises(RegistrationError):
            registration_page.pass_registration(username=username, email=email, password=password)
    with allure.step("Try to authorize"):
        authorization_page = registration_page.go_to_authorization_page()
        with pytest.raises(AuthorizationError):
            authorization_page.authorize(username=username, password=password)
    with allure.step("Accept user"):
        response = api_client.accept_user(username)
        attach_http(response)
    with allure.step('User was redirected to main page after refresh'):
        authorization_page.refresh()
        assert 'welcome' in urlparse(authorization_page.current_url).path
    with allure.step("Delete user"):
        api_client.del_user(username)
        attach_http(response)
    with allure.step("User was redirected from main page after refresh"):
        main_page.refresh()
        assert 'welcome' not in urlparse(authorization_page.current_url).path
    with allure.step("Try to authorize"):
        authorization_page.make_request()
        with pytest.raises(AuthorizationError):
            authorization_page.authorize(username=username, password=password)
    with allure.step("Pass registration"):
        registration_page.make_request()
        registration_page.pass_registration(username=username, email=email, password=password)


@pytest.mark.API
@pytest.mark.scenario
def test_scenario2(api_client: ApiClient):
    """Test scenario with several requests

    Steps:
        0 Generate credentials
        1 Delete user via del_user API function (user not exists)
        2 Block user via block_user API function (user not exists)
        3 Accept user via accept_user API function (user not exists)
        4 Add user via add_user API function with credentials
        5 Accept user via accept_user API function
        6 Block user via block_user API function
        7 Block user via block_user API function
        8 Accept user via accept_user API function
        9 Accept user via accept_user API function
        0 Delete user via del_user API function
        1 Add user via add_user API function with the same credentials
        2 Add user via add_user API function
        3 Add user via add_user API function with different email
        4 Add user via add_user API function with different username

    Expected results:
        Steps 1-3 fail, status code 404
        Step 4 succeed, status code 201
        Step 5 status code 304
        Step 6 status code 200
        Step 7 status code 304
        Step 8 status code 200
        Step 9 status code 304
        Step 10 status code 204
        Step 11 status code 201
        Step 12 status code 304
        Step 13 status code 304
        Step 14 status code 304
    """

    username = 'my-username'
    email = 'my-email@gmail.com'
    password = 'I love eating pizza'

    with allure.step(f"Del user {username} who doesn't exist"):
        response = api_client.del_user(username)
        attach_http(response)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f"Block user {username} who doesn't exist"):
        response = api_client.block_user(username)
        attach_http(response)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f"Accept user {username} who doesn't exist"):
        response = api_client.accept_user(username)
        attach_http(response)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f'Add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        attach_http(response)
        assert response.status_code == status_codes.CREATED
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        attach_http(response)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Block user {username}"):
        response = api_client.block_user(username)
        attach_http(response)
        assert response.status_code == status_codes.OK
    with allure.step(f"Block user {username} again"):
        response = api_client.block_user(username)
        attach_http(response)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        attach_http(response)
        assert response.status_code == status_codes.OK
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        attach_http(response)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Del user {username}"):
        response = api_client.del_user(username)
        attach_http(response)
        assert response.status_code == status_codes.DELETED
    with allure.step(f'Add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        attach_http(response)
        assert response.status_code == status_codes.CREATED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        attach_http(response)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email='a' + email, password=password)
        attach_http(response)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username='a' + username, email=email, password=password)
        attach_http(response)
        assert response.status_code == status_codes.NOT_CHANGED
