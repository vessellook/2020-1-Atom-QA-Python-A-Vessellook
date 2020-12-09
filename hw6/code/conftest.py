import pytest

from application.error_handler import ErrorHandler
from application.my_http_server import MyHttpServer
from application.app_handler import AppHandler
from application.mock_handler import MockHandler
from settings import APP_INFO, MOCK_SERVICE_INFO, NOT_CREATED_SERVICE_INFO, NOT_STARTED_SERVICE_INFO, set_service_url, \
    ERROR_SERVICE_INFO


@pytest.fixture(scope='session')
def mock_service_info():
    set_service_url(MOCK_SERVICE_INFO.root_url())
    mock_server = MyHttpServer(MOCK_SERVICE_INFO, MockHandler)
    mock_server.start()
    yield MOCK_SERVICE_INFO
    mock_server.stop()


@pytest.fixture(scope='session')
def not_created_service_info():
    set_service_url(NOT_CREATED_SERVICE_INFO.root_url())
    return NOT_CREATED_SERVICE_INFO


@pytest.fixture(scope='session')
def not_started_service_info():
    set_service_url(NOT_STARTED_SERVICE_INFO.root_url())
    not_started_server = MyHttpServer(NOT_STARTED_SERVICE_INFO, MockHandler)
    yield NOT_STARTED_SERVICE_INFO
    not_started_server.stop()


@pytest.fixture(scope='session')
def error_service_info():
    set_service_url(ERROR_SERVICE_INFO.root_url())
    error_server = MyHttpServer(ERROR_SERVICE_INFO, ErrorHandler)
    error_server.start()
    yield ERROR_SERVICE_INFO
    error_server.stop()


@pytest.fixture(scope='session')
def app_info():
    app_server = MyHttpServer(APP_INFO, AppHandler)
    app_server.start()
    yield APP_INFO
    app_server.stop()
