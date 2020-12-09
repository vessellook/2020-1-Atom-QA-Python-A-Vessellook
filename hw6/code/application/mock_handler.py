import json
from urllib.parse import urlparse, parse_qs

from application.my_handler import MyHandler
from application.utils import jsonify


class MockHandler(MyHandler):
    _chats = set()

    def _make_error_response(self):
        self.make_response(code=400, headers={'Content-Type': 'application/json'},
                           data=jsonify({
                               'ok': False,
                               'error_code': 400,
                               'description': 'Bad Request: some details'
                           }))

    def _make_unathorized_response(self):
        self.make_response(code=401)

    def _make_method_not_allowed_response(self):
        self.make_response(code=405)

    def _make_normal_response(self, text: str):
        self.make_response(code=200, headers={'Content-Type': 'application/json'},
                           data=jsonify({
                               'ok': True,
                               'result': {
                                   'message_id': 1,
                                   'date': 1,
                                   'text': text,
                                   'chat': {
                                       'id': 1,
                                       'type': 'private'
                                   }
                               }
                           }))

    def do_GET(self):
        if self.path == '/':
            self.make_response(code=200, headers=dict({'Content-Type': 'application/json'}),
                               json={'hello': 'client', "I'm": 'mock'})
        if '/sendMessage' in self.path:
            if 'Authorization' not in self.headers:
                self._make_method_not_allowed_response()
                return
            params = parse_qs(urlparse(self.path).query)
            if 'chat_id' not in params or 'text' not in params:
                self._make_error_response()
            if params['chat_id'] in self._chats:
                self._make_normal_response(params['text'][0])
            else:
                self._make_unathorized_response()
        else:
            self._make_error_response()

    def do_POST(self):
        result = urlparse(self.path)
        if '/sendMessage' in result.path:
            if 'Authorization' not in self.headers:
                self._make_method_not_allowed_response()
                return
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                params = json.loads(post_data.decode())
                if 'chat_id' not in params or 'text' not in params:
                    self._make_error_response()
                if str(params['chat_id']) in self._chats:
                    self._make_normal_response(params['text'])
                else:
                    self._make_unathorized_response()
            except (KeyError, ValueError) as e:
                print(e.__traceback__)
                self._make_error_response()
        else:
            self._make_error_response()

    def do_PUT(self):
        # этот метод используется только для добавления чатов в тестах
        if self.path == '/addChat':
            self._chats.add(self.headers['Chat'])
        elif self.path == '/removeChat':
            self._chats.discard(self.headers['Chat'])
        self.make_response()
