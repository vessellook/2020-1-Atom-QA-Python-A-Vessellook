from urllib.parse import urlparse

import requests
from selenium.common.exceptions import WebDriverException
import pytest

from utils.not_raises import not_raises
from clients.api_client import ApiClient
from ui.pages.registration_page import RegistrationPage, RegistrationError
from ui.pages.authorization_page import AuthorizationPage, AuthorizationError
from utils import make, status_codes


@pytest.mark.mixed
def test_add_some_path(api_client: ApiClient):
    response = requests.get(f'http://{api_client.netloc}/haha', timeout=0.5,
                             cookies=api_client.cookies, headers=api_client.headers)
    assert response.status_code == 404


@pytest.mark.mixed
def test_api_after_registration(registration_page: RegistrationPage, settings):
    username, email, password = make.auth_data()
    main_page = registration_page.pass_registration(username=username, email=email,
                                                    password=password)
    assert main_page.session_cookie is not None
    api_client = ApiClient(admin_keys=ApiClient.Keys(main_page.session_cookie,
                                                     main_page.user_agent),
                           netloc=settings.app_netloc)
    response = api_client.accept_user(username)
    assert response.status_code != status_codes.NOT_AUTHORIZED


@pytest.mark.mixed
def test_ui_after_api_add_user(authorization_page: AuthorizationPage,
                               api_client: ApiClient):
    username, email, password = make.auth_data()
    response = api_client.set_vk_id(username=username, email=email, password=password)
    assert response.status_code in range(200, 400)
    with not_raises(WebDriverException):
        main_page = authorization_page.authorize(username=username, password=password)
    assert 'welcome' in urlparse(main_page.current_url).path


@pytest.mark.scenario
@pytest.mark.mixed
def test_scenario(registration_page: RegistrationPage, api_client: ApiClient):
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
