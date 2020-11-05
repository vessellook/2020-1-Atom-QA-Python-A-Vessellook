from client.http_request import HttpRequest
from client.http_client import HttpClient

from settings import APP_HOST, APP_PORT


def main():
    client = HttpClient(APP_HOST, APP_PORT)
    request = HttpRequest('GET', '/')
    response = client.send(request)
    print(response.body)


if __name__ == '__main__':
    main()
