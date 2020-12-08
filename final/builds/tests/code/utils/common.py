from urllib.parse import urlparse, urlunparse

import allure
from requests import Response


def change_netloc(url, netloc):
    parsed = urlparse(url)
    changed = parsed._replace(netloc=netloc)  # noqa:
    return urlunparse(changed)


def attach_http(response: Response, name: str = ''):
    if len(name) == 0:
        name = '-' + name
    req = response.request
    req_first_line = f'{req.method} {req.path_url} HTTP/{response.raw.version / 10}'
    req_headers = '\n'.join([f"{name}: {value}" for name, value in req.headers.items()])
    req_str = f'{req_first_line}\n{req_headers}\n\n'
    if req.body is not None:
        req_str += str(req.body)
    allure.attach(req_str, attachment_type=allure.attachment_type.TEXT, name=f'request{name}.txt')
    res_first_line = f'HTTP/{response.raw.version / 10} {response.status_code} {response.reason}'
    res_headers = '\n'.join([f"{name}: {value}" for name, value in response.headers.items()])
    res_str = f'{res_first_line}\n{res_headers}\n\n'
    if response.text is not None:
        req_str += response.text
    allure.attach(res_str, attachment_type=allure.attachment_type.TEXT, name=f'response_{name}.txt')
