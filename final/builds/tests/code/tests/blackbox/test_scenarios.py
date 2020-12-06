from urllib.parse import urlparse

import allure
import pytest

from clients.api_client import ApiClient
from ui.pages.registration_page import RegistrationPage, RegistrationError
from ui.pages.authorization_page import AuthorizationError
from utils import make, status_codes


@pytest.mark.scenario
def test_scenario1(registration_page: RegistrationPage, api_client: ApiClient):
    username, email, password = make.auth_data()
    main_page = registration_page.pass_registration(username=username, password=password,
                                                    email=email)
    api_client.block_user(username)
    main_page.refresh()
    assert 'welcome' not in urlparse(main_page.current_url).path
    registration_page.make_request()
    with pytest.raises(RegistrationError):
        registration_page.pass_registration(username=username, email=email, password=password)
    authorization_page = registration_page.go_to_authorization_page()
    with pytest.raises(AuthorizationError):
        authorization_page.authorize(username=username, password=password)
    api_client.accept_user(username)
    authorization_page.refresh()
    assert 'welcome' in urlparse(authorization_page.current_url).path
    api_client.del_user(username)
    main_page.refresh()
    assert 'welcome' not in urlparse(authorization_page.current_url).path
    authorization_page.make_request()
    with pytest.raises(AuthorizationError):
        authorization_page.authorize(username=username, password=password)
    registration_page.make_request()
    registration_page.pass_registration(username=username, email=email, password=password)


@pytest.mark.API
@pytest.mark.scenario
def test_scenario2(api_client: ApiClient):
    """Test with several requests"""

    username = 'my-username'
    email = 'my-email@gmail.com'
    password = 'I love eating pizza'

    with allure.step(f"Del user {username} who doesn't exist"):
        response = api_client.del_user(username)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f"Block user {username} who doesn't exist"):
        response = api_client.block_user(username)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f"Accept user {username} who doesn't exist"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f'Add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == status_codes.CREATED
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Block user {username}"):
        response = api_client.block_user(username)
        assert response.status_code == status_codes.OK
    with allure.step(f"Block user {username} again"):
        response = api_client.block_user(username)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.OK
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Del user {username}"):
        response = api_client.del_user(username)
        assert response.status_code == status_codes.DELETED
    with allure.step(f'Add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == status_codes.CREATED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email='a' + email, password=password)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username='a' + username, email=email, password=password)
        assert response.status_code == status_codes.NOT_CHANGED
