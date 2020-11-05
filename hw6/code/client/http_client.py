from contextlib import contextmanager
from socket import socket, SOCK_STREAM, AF_INET

from client.http_request import HttpRequest
from client.http_response import HttpResponse


class HttpClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @staticmethod
    def _get_message(sock: socket, bufsize: int = 4096):
        data = bytes()
        while buff := sock.recv(bufsize):
            data += buff
        message = data.decode(encoding='UTF-8')
        return message

    @contextmanager
    def _connect(self) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.1)
        sock.connect((self.host, self.port))
        yield sock
        sock.close()

    def send(self, request: HttpRequest):
        with self._connect() as sock:
            sock.sendall(bytes(request))
            message = self._get_message(sock)
            return HttpResponse.from_str(message)
