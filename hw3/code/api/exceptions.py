class WrongResponseStatusCodeException(Exception):
    def __init__(self,
                 got_status_code: int,
                 expected_status_code: int,
                 reason: str,
                 url: str):
        Exception.__init__(self, f'Got {got_status_code} {reason} for {url}; '
                                 f'expected {expected_status_code}')


class CsrfTokenNotReceivedException(Exception):
    pass
