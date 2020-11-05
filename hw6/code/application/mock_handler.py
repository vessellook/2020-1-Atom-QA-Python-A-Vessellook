import json
from urllib.parse import urljoin
from http.server import BaseHTTPRequestHandler


class MockHandler(BaseHTTPRequestHandler):

    def make_response(self, headers: dict = None, data: bytes = None, code: int = 200):
        self.send_response(code)
        if headers is None:
            headers = {}
        if data is not None:
            headers['Content-Length'] = len(data)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()
        if data is not None:
            self.wfile.write(data)

    def do_GET(self):
        self.make_response(code=200, headers={'Content-Type': 'application/json'},
                           data=json.dumps('hello').encode())

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.make_response(code=404, headers={'Content-Type': 'application/json'},
                               data=json.dumps('hello').encode())
        except (ValueError, KeyError) as e:
            print(e.__traceback__)

    def do_PUT(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.make_response(code=404, headers={'Content-Type': 'application/json'},
                               data=json.dumps('hello').encode())
        except (ValueError, KeyError) as e:
            print(e.__traceback__)
