import json
from logging import Logger

import allure
import requests

from api.exceptions import WrongResponseStatusCodeException, CsrfTokenNotReceivedException


def print_response(response):
    print('\n', response.url)
    print(response.status_code)
    print(response.request.headers)
    print(response.headers)
    print(response.cookies.get_dict())
    print(response.text[:1000])


class MyTargetClient:
    def __init__(self, logger: Logger, email: str, password: str):
        self.logger = logger
        self.session = requests.session()
        self.csrf_token = None
        self.email = email
        self.password = password

    @allure.step('auth to target.my.com')
    def auth(self):
        """Creates request to target.my.com to get access to user's account and to manage user's data"""
        self._request('GET', 'https://target.my.com/')
        self._request('POST', 'https://auth-ac.my.com/auth',
                      headers={'Content-Type': 'application/x-www-form-urlencoded',
                               'Referer': 'https://target.my.com/'
                               },
                      data={
                          'email': self.email,
                          'password': self.password,
                          'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1#email'
                      })
        self._request_token()

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
        return response.json()['id']

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

    @allure.step('get list of segments')
    def get_segments_list(self, limit: int):
        url = f'https://target.my.com/api/v2/remarketing/segments.json?limit={limit}'
        referer = 'https://target.my.com/segments/segments_list'
        response = self._request('GET', url,
                                 headers={
                                     'X-CSRFToken': self.csrf_token,
                                     'Referer': referer
                                 })
        json_object = json.loads(response.text)
        result = []
        for item in json_object['items']:
            result.append(item['id'])
        return result

    def _request_token(self):
        response = self._request('GET', 'https://target.my.com/csrf/')
        cookies = response.cookies.get_dict()
        if 'csrftoken' not in cookies:
            raise CsrfTokenNotReceivedException
        self.csrf_token = cookies['csrftoken']
        return self.csrf_token

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
        self.logger.info('START REQUEST')
        self.logger.info(f'status code = {response.status_code}')
        self.logger.info(f'URL = {response.url}')
        self.logger.info(f'request.headers = {response.request.headers}')
        self.logger.info(f'response.headers = {response.headers}')
        self.logger.info(f'response.cookies = {response.cookies}')
        self.logger.info(f'response.text[:1000] = {response.text[:1000]}')
        self.logger.info('STOP REQUEST')
