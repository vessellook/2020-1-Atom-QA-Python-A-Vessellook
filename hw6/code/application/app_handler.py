"""This script contains simple Telegram Bot which sends messages to Telegram"""

from urllib.parse import urljoin

import requests

from application.my_handler import MyHandler
from application.utils import unjsonify, generate_token
from settings import get_service_url


class AppHandler(MyHandler):
    _chats = {}
    _tokens = {}

    def _make_error_response(self):
        self.make_response(code=400, headers=dict({'Content-Type': 'application/json'}),
                           json={'error': 'bad request'})

    def do_GET(self):
        if self.path == '/':
            self.make_response(code=200, headers=dict({'Content-Type': 'application/json'}),
                               json={'hello': 'client', "I'm": 'application'})
        else:
            self._make_error_response()

    def do_POST(self):
        if self.path == '/send':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                obj = unjsonify(post_data)
                token = obj['token']
                message = str(obj['message'])
                headers = {}
                if 'Authorization' in self.headers:
                    headers['Authorization'] = self.headers['Authorization']
                response = requests.post(urljoin(get_service_url(), '/sendMessage'),
                                         headers=headers,
                                         json={'chat_id': self._chats[token],
                                               'text': message})
                self.make_response(code=response.status_code, headers=dict(response.headers),
                                   data=response.text.encode())
                return
            except (ValueError, KeyError) as e:
                print(e.__traceback__)
        self._make_error_response()

    def do_PUT(self):
        if self.path == '/tokens':
            try:
                content_length = int(self.headers['Content-Length'])
                data = self.rfile.read(content_length)
                obj = unjsonify(data)
                chat_id = obj['chat_id']
                token = self._tokens.get(chat_id, None)
                if token is None:
                    token = generate_token()
                    self._tokens[chat_id] = token
                    self._chats[token] = chat_id
                self.make_response(code=200, headers=dict({'Content-Type': 'application/json'}),
                                   json={'token': token})
                return
            except (ValueError, KeyError) as e:
                print(e.__traceback__)
        self._make_error_response()
