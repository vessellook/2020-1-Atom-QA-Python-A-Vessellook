from http.server import BaseHTTPRequestHandler

from application.utils import jsonify


class MyHandler(BaseHTTPRequestHandler):
    def make_response(self, headers: dict = None, data: bytes = None, json=None, code: int = 200):
        if json is not None and data is None:
            data = jsonify(json)
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
