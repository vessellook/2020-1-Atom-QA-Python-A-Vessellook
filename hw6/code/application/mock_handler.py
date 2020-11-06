import json
from urllib.parse import urlparse, parse_qs

from application.my_handler import MyHandler
from application.utils import jsonify


class MockHandler(MyHandler):
    _chats = set()

    def add_chat(self, chat_id: int):
        self._chats.add(str(chat_id))

    def _make_error_response(self):
        self.make_response(code=400, headers={'Content-Type': 'application/json'},
                           data=jsonify({
                               'ok': False,
                               'error_code': 400,
                               'description': 'Bad Request: some details'
                           }))

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
        result = urlparse(self.path)
        result2 = parse_qs(result.query)
        if self.path == '/':
            self.make_response(code=200, headers=dict({'Content-Type': 'application/json'}),
                               data=jsonify({'hello': 'client', "I'm": 'mock'}))
        if '/sendMessage' in result.path:
            try:
                if result2['chat_id'] in self._chats and 'text' in result2:
                    self._make_normal_response(result2['text'][0])
                    return
            except (KeyError, ValueError) as e:
                print(e.__traceback__)
        self._make_error_response()

    def do_POST(self):
        result = urlparse(self.path)
        if '/sendMessage' in result.path:
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                obj = json.loads(post_data.decode())
                if obj['chat_id'] in self._chats and 'text' in obj:
                    self._make_normal_response(obj['text'])
                    return
            except (KeyError, ValueError) as e:
                print(e.__traceback__)
        self._make_error_response()

    # def do_PUT(self):
    #     try:
    #         content_length = int(self.headers['Content-Length'])
    #         put_data = self.rfile.read(content_length)
    #         self.make_response(code=404, headers={'Content-Type': 'application/json'},
    #                            data=json.dumps('hello').encode())
    #     except (ValueError, KeyError) as e:
    #         print(e.__traceback__)
