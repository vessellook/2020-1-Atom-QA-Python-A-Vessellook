import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable


class MyHttpServer:
    def __init__(self, host, port, handler: Callable[..., BaseHTTPRequestHandler]):
        self.host = host
        self.port = port
        self.stop_server = False
        self.handler = handler
        self.server = HTTPServer((host, port), self.handler)

    def start(self):
        self.server.allow_reuse_address = True
        th = threading.Thread(target=self.server.serve_forever)
        th.start()
        return self.server

    def stop(self):
        self.server.server_close()

        self.server.shutdown()
