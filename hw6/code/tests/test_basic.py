import json
import socket

import pytest

from client.http_client import HttpClient
from client.http_request import HttpRequest
from settings import ServerInfo


def add_chat(chat_id: int, info: ServerInfo):
    client = HttpClient(info.host, info.port)
    client.send(HttpRequest('PUT', '/addChat', headers={'Chat': chat_id}))


def remove_chat(chat_id: int, info: ServerInfo):
    client = HttpClient(info.host, info.port)
    client.send(HttpRequest('PUT', '/removeChat', headers={'Chat': chat_id}))


def get_token(chat_id: int, info: ServerInfo):
    client = HttpClient(info.host, info.port)
    response = client.send(HttpRequest('PUT', '/tokens',
                                       headers={'Content-Type': 'application/json'},
                                       body=json.dumps({'chat_id': chat_id})))
    return response.json()['token']


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
        token = get_token(0, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': 'text...'})))
        assert response.status_code == 500


class TestAuthorizationHeader:
    # @pytest.mark.skip
    def test_without_authorization(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(1, mock_service_info)
        token = get_token(1, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': 'text...'})))
        assert response.status_code == 405

    # @pytest.mark.skip
    def test_without_authorization_2(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        remove_chat(2, mock_service_info)
        token = get_token(2, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': 'text...'})))
        assert response.status_code == 405

    # @pytest.mark.skip
    def test_with_authorization(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(3, mock_service_info)
        token = get_token(3, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': 'text...'})))
        assert response.status_code == 200

    # @pytest.mark.skip
    def test_with_authorization_2(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        remove_chat(4, mock_service_info)
        token = get_token(4, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': 'text...'})))
        assert response.status_code == 401


class TestApplication:
    # @pytest.mark.skip
    def test_without_token(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(5, mock_service_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'message': 'text...'})))
        assert response.status_code == 400

    # @pytest.mark.skip
    def test_without_message(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(6, mock_service_info)
        token = get_token(6, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token})))
        assert response.status_code == 400

    # @pytest.mark.skip
    def test_wrong_token(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(7, mock_service_info)
        token = get_token(7, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token + '1'})))
        assert response.status_code == 400

    def test_empty_message(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(8, mock_service_info)
        token = get_token(8, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': ''})))
        assert response.status_code == 200

    # @pytest.mark.skip
    def test_wrong_message_type(self, app_info: ServerInfo, mock_service_info: ServerInfo):
        add_chat(9, mock_service_info)
        token = get_token(9, app_info)
        client = HttpClient(app_info.host, app_info.port)
        response = client.send(HttpRequest('POST', '/send',
                                           headers={'Authorization': 'something',
                                                    'Content-Type': 'application/json'},
                                           body=json.dumps({'token': token,
                                                            'message': 1})))
        assert response.status_code == 200
