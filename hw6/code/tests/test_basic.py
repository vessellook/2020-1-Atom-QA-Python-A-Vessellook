import json
import socket

import pytest

from client.http_client import HttpClient
from client.http_request import HttpRequest
from settings import ServerInfo


class TestMockErrors:
    # проверка, что приложение поднято, а мок не поднят
    # @pytest.mark.skip
    def test_mock_up(self, app_info: ServerInfo, not_created_service_info: ServerInfo):
        app_client = HttpClient(app_info.host, app_info.port)
        app_client.send(HttpRequest('GET', '/'))
        mock_client = HttpClient(not_created_service_info.host, not_created_service_info.port)
        with pytest.raises(ConnectionRefusedError):
            mock_client.send(HttpRequest('GET', '/'))

    # проверка, что мок поднят, но не отвечает
    # @pytest.mark.skip
    def test_mock_timeout(self, app_info: ServerInfo, not_started_service_info: ServerInfo):
        app_client = HttpClient(app_info.host, app_info.port)
        app_client.send(HttpRequest('GET', '/'))
        mock_client = HttpClient(not_started_service_info.host, not_started_service_info.port)
        with pytest.raises(socket.timeout):
            mock_client.send(HttpRequest('GET', '/'))

    # проверка, что мок отдаёт приложению 500
    # @pytest.mark.skip
    def test_mock_500(self, app_info: ServerInfo, error_service_info: ServerInfo):
        app_client = HttpClient(app_info.host, app_info.port)
        response = app_client.send(HttpRequest('PUT', '/tokens',
                                               headers={'Content-Type': 'application/json'},
                                               body=json.dumps({'chat_id': 0})))
        token = response.json()['token']
        response2 = app_client.send(HttpRequest('POST', '/send',
                                                headers={'Authorization': 'something',
                                                         'Content-Type': 'application/json'},
                                                body=json.dumps({'token': token,
                                                                 'message': 'text...'})))
        assert response2.status_code == 500
