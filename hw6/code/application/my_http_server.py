import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable

from settings import ServerInfo


class MyHttpServer:
    def __init__(self, info: ServerInfo, handler: Callable[..., BaseHTTPRequestHandler]):
        self.host = info.host
        self.port = info.port
        self.stop_server = False
        self.running = False
        self.handler = handler
        self.server = HTTPServer((info.host, info.port), self.handler)

    def start(self):
        if not self.running:
            self.server.allow_reuse_address = True
            self.running = True
            th = threading.Thread(target=self.server.serve_forever)
            th.start()
        return self.host, self.port

    def stop(self):
        if self.running:
            self.running = False
            self.server.server_close()
            self.server.shutdown()
