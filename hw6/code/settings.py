from dataclasses import dataclass

@dataclass
class ServerInfo:
    host: str
    port: int

    def root_url(self):
        return f'http://{self.host}:{self.port}'


APP_INFO = ServerInfo('127.0.0.1', 1050)

MOCK_SERVICE_INFO = ServerInfo('127.0.0.1', 1051)

NOT_STARTED_SERVICE_INFO = ServerInfo('127.0.0.1', 1052)

NOT_CREATED_SERVICE_INFO = ServerInfo('127.0.0.1', 1053)

ERROR_SERVICE_INFO = ServerInfo('127.0.0.1', 1054)


SERVICE_URL = MOCK_SERVICE_INFO.root_url()


def get_service_url():
    return SERVICE_URL


def set_service_url(service_url: str):
    global SERVICE_URL
    SERVICE_URL = service_url
