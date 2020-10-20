import json
from logging import Logger
from typing import List

import allure
import requests

from api.exceptions import WrongResponseStatusCodeException, CsrfTokenNotReceivedException, \
    JsonBadFormatException


class MyTargetClient:
    MAX_VALUE_LIMIT = 500

    def __init__(self, logger: Logger, email: str, password: str):
        self.logger = logger
        self.session = requests.session()
        self.csrf_token = None
        self.email = email
        self.password = password

    @allure.step('auth to target.my.com')
    def auth(self):
        """Creates request to target.my.com to get access to user's account and to manage user's data"""
        main_page_url = 'https://target.my.com/'
        auth_url = 'https://auth-ac.my.com/auth'
        continue_url = 'https://target.my.com/auth/mycom?state=target_login%3D1#email'

        self._request('GET', main_page_url)
        self._request('POST', auth_url,
                      headers={'Content-Type': 'application/x-www-form-urlencoded',
                               'Referer': main_page_url
                               },
                      data={
                          'email': self.email,
                          'password': self.password,
                          'continue': continue_url
                      })
        self.csrf_token = self._request_token()

    @allure.step('create segment with name {segment_name}')
    def create_segment(self, segment_name) -> int:
        """Creates request to target.my.com to create segment. Returns id of created request"""
        url = 'https://target.my.com/api/v2/remarketing/segments.json'
        referer = 'https://target.my.com/segments/segments_list'
        response = self._request('POST', url,
                                 headers={'Content-Type': 'application/json',
                                          'X-CSRFToken': self.csrf_token,
                                          'Referer': referer
                                          },
                                 data={"name": segment_name,
                                       "pass_condition": 1,
                                       "relations": [{
                                           "object_type": "remarketing_player",
                                           "params": {
                                               "type": "positive",
                                               "left": 365,
                                               "right": 0}
                                       }]
                                       },
                                 is_json=True)
        response_json = response.json()
        if 'id' not in response_json:
            raise JsonBadFormatException('no "id" in json')
        return response_json['id']

    @allure.step('create segment with id {segment_id}')
    def delete_segment(self, segment_id):
        url = f'https://target.my.com/api/v2/remarketing/segments/{segment_id}.json'
        referer = 'https://target.my.com/segments/segments_list'
        self._request('DELETE', url,
                      headers={
                          'X-CSRFToken': self.csrf_token,
                          'Referer': referer
                      },
                      status_code=204)

    @allure.step('check segment presence with id {segment_id}')
    def has_segment(self, segment_id) -> bool:
        count = self._get_segment_count()
        response_count = (count - 1) // self.MAX_VALUE_LIMIT + 1
        for i in range(response_count):
            segment_id_list = self._get_segment_id_list(limit=self.MAX_VALUE_LIMIT,
                                                        offset=self.MAX_VALUE_LIMIT * i)
            try:
                segment_id_list.index(segment_id)
                return True
            except ValueError:
                pass
        return False

    @allure.step('get count of segments')
    def _get_segment_count(self) -> int:
        url = f'https://target.my.com/api/v2/remarketing/segments.json'
        referer = 'https://target.my.com/segments/segments_list'
        response = self._request('GET', url,
                                 headers={
                                     'X-CSRFToken': self.csrf_token,
                                     'Referer': referer
                                 })
        json_object = json.loads(response.text)
        if 'count' not in json_object:
            raise JsonBadFormatException('no "count" in json')
        return int(json_object['count'])

    @allure.step('get list of segments')
    def _get_segment_id_list(self, limit: int = 20, offset: int = 0) -> List[int]:
        url = f'https://target.my.com/api/v2/remarketing/segments.json?limit={limit}&offset={offset}'
        referer = 'https://target.my.com/segments/segments_list'
        response = self._request('GET', url,
                                 headers={
                                     'X-CSRFToken': self.csrf_token,
                                     'Referer': referer
                                 })
        json_object = json.loads(response.text)
        result = []
        if 'items' not in json_object:
            raise JsonBadFormatException('no "items" in json')
        for item in json_object['items']:
            if 'id' not in item:
                raise JsonBadFormatException('no "id" in json')
            result.append(int(item['id']))
        return result

    def _request_token(self):
        csrf_url = 'https://target.my.com/csrf/'
        response = self._request('GET', csrf_url)
        cookies = response.cookies.get_dict()
        if 'csrftoken' not in cookies:
            raise CsrfTokenNotReceivedException
        return cookies['csrftoken']

    def _request(self,
                 method: str,
                 url: str,
                 status_code=200,
                 headers=None,
                 params=None,
                 data=None,
                 is_json=False):
        """Wrap for self.session.request for logging"""
        if is_json:
            response = self.session.request(method, url, headers=headers, params=params, json=data)
        else:
            response = self.session.request(method, url, headers=headers, params=params, data=data)
        self._log(response)
        if response.status_code != status_code:
            raise WrongResponseStatusCodeException(got_status_code=response.status_code,
                                                   reason=response.reason,
                                                   expected_status_code=status_code,
                                                   url=url)
        return response

    def _log(self, response):
        """Logging format"""
        self.logger.info('START REQUEST')
        self.logger.info(f'status code = {response.status_code}')
        self.logger.info(f'URL = {response.url}')
        self.logger.info(f'request.headers = {response.request.headers}')
        self.logger.info(f'response.headers = {response.headers}')
        self.logger.info(f'response.cookies = {response.cookies}')
        self.logger.info(f'response.text[:1000] = {response.text[:1000]}')
        self.logger.info('STOP REQUEST')
