import pytest
from application.http_server import MyHttpServer
from application.app_handler import AppHandler
from application.mock_handler import MockHandler
from settings import APP_HOST, APP_PORT, STUB_HOST, STUB_PORT


@pytest.fixture(scope='session', autouse=True)
def setup():
    mock_server = MyHttpServer(STUB_HOST, STUB_PORT, MockHandler)
    mock_server.start()
    app_server = MyHttpServer(APP_HOST, APP_PORT, AppHandler)
    app_server.start()
    yield
    app_server.stop()
    mock_server.stop()
