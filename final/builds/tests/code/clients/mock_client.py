"""Module with class to connect to mock server"""
from typing import Any

import allure
import requests


class MockClient:
    """Class to connect to mock server"""

    def __init__(self, netloc, timeout=1):
        """:param timeout:
            set max timeout for all requests"""
        self.netloc = netloc
        self._timeout = timeout

    @allure.step("Set vk_id {vk_id} for user {username}")
    def set_vk_id(self, username: str, vk_id: Any):
        """Order mock server to add user with vk_id

        If user exists, overwrite him"""
        return requests.put(f'http://{self.netloc}/mock/add_user/{username}',
                            json={"vk_id": vk_id},
                            timeout=self._timeout)

    @allure.step("Remove vk_id to user {username}")
    def unset_vk_id(self, username: str):
        """Order mock server to remove user vk_id

        If user don't have vk_id, do nothing"""
        return requests.delete(f'http://{self.netloc}/mock/remove_user/{username}',
                               timeout=self._timeout)

    @allure.step("Set special response for user {username}")
    def set_response(self, username: str, code: int, data: str = None, json: Any = None):
        """Order mock server to add specific response to user

        If user exists, it will rewrite him"""
        obj = {'code': code}
        if json is not None:
            obj['json'] = json
        if data is not None:
            obj['data'] = data
        return requests.put(f'http://{self.netloc}/mock/set_response/{username}',
                            json=obj, timeout=self._timeout)

    @allure.step("Remove any special response for user {username}")
    def unset_response(self, username: str):
        """Order mock server to remove user (delete vk_id)"""
        return requests.delete(f'http://{self.netloc}/mock/unset_response/{username}',
                               timeout=self._timeout)
