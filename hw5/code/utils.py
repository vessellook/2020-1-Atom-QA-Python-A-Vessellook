from dataclasses import dataclass
from datetime import datetime

from faker import Faker


@dataclass(frozen=True)
class LogsRecord:
    ip: str
    method: str
    location: str
    status_code: int
    response_size: int
    time: datetime

    @staticmethod
    def fake(faker: Faker):
        ip = '.'.join([str(faker.random_int(0, 5)) for _ in range(4)])
        methods = ['GET', 'POST', 'PUT', 'HEAD', 'PATCH', 'DELETE']
        method = methods[faker.random_int(0, len(methods))]
        location = '/' + '/'.join([faker.word() for _ in range(faker.random_int(0, 5))])
        status_code = faker.random_int(200, 600)
        response_size = faker.random_int()
        time = faker.past_datetime()
        return LogsRecord(ip=ip, method=method, location=location, status_code=status_code,
                          response_size=response_size, time=time)


class InvalidIdException(Exception):
    pass
