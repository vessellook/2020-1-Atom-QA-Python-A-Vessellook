"""Module with class to call myapp API functions"""
from collections import namedtuple
from typing import Optional

import allure
import requests


class ApiClient:
    """Class to connect to call myapp API functions"""
    Keys = namedtuple('Keys', 'session agent')
    netloc = ''
    admin_keys = Keys('', '')

    def __init__(self, keys: Optional[Keys], timeout=2):
        """Session cookie and User-Agent header require to authorized access"""
        self._timeout = timeout
        if keys is None:
            keys = self.admin_keys
        self.cookies = {'session': keys.session}
        self.headers = {'User-Agent': keys.agent}

    @allure.step('Call add_user API function of myapp')
    def add_user(self, username: str, email: str, password: str) -> requests.Response:
        """Call add_user API function"""
        return requests.post(f'http://{self.netloc}/api/add_user',
                             cookies=self.cookies,
                             headers=self.headers,
                             json={
                                 "username": username,
                                 "password": password,
                                 "email": email},
                             timeout=self._timeout)

    @allure.step('Call del_user API function of myapp')
    def del_user(self, username: str) -> requests.Response:
        """Call del_user API function"""
        return requests.get(f'http://{self.netloc}/api/del_user/{username}',
                            cookies=self.cookies,
                            headers=self.headers,
                            timeout=self._timeout)

    @allure.step('Call block_user API function of myapp')
    def block_user(self, username: str) -> requests.Response:
        """Call block_user API function"""
        return requests.get(f'http://{self.netloc}/api/block_user/{username}',
                            cookies=self.cookies,
                            headers=self.headers,
                            timeout=self._timeout)

    @allure.step('Call accept_user API function of myapp')
    def accept_user(self, username: str) -> requests.Response:
        """Call accept_user API function"""
        return requests.get(f'http://{self.netloc}/api/accept_user/{username}',
                            cookies=self.cookies,
                            headers=self.headers,
                            timeout=self._timeout)

    @allure.step('Call status API function of myapp')
    def get_status(self) -> requests.Response:
        """Call status API function"""
        return requests.get(f'http://{self.netloc}/status',
                            cookies=self.cookies,
                            headers=self.headers,
                            timeout=self._timeout)
