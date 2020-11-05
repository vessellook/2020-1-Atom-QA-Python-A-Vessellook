from urllib.parse import urljoin
from http.server import BaseHTTPRequestHandler

import requests

from settings import STUB_URL


class AppHandler(BaseHTTPRequestHandler):

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
        response = requests.get(urljoin(STUB_URL, self.path))
        self.make_response(code=response.status_code, headers=dict(response.headers),
                           data=response.text.encode())

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            response = requests.post(urljoin(STUB_URL, self.path), post_data)
            self.make_response(code=response.status_code, headers=dict(response.headers),
                               data=response.text.encode())
        except (ValueError, KeyError) as e:
            print(e.__traceback__)

    def do_PUT(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            response = requests.put(urljoin(STUB_URL, self.path), post_data)
            self.make_response(code=response.status_code, headers=dict(response.headers),
                               data=response.text.encode())
        except (ValueError, KeyError) as e:
            print(e.__traceback__)
