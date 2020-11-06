from dataclasses import dataclass, field
from typing import Optional
import json
import re


@dataclass
class HttpResponse:
    status_code: int
    headers: dict = field(default_factory=list)
    body: Optional[str] = None
    version: str = '1.0'

    def json(self):
        return json.loads(self.body)

    @staticmethod
    def from_str(message: str):
        lines = message.split('\n')
        _, version, status_code, _ = re.split(r'HTTP/(.*) ([2-5][0-9]{2}) .*', lines[0])
        body = None
        headers = {}
        for num, line in enumerate(lines[1:]):
            if len(line.strip()) == 0:
                body = '\n'.join(lines[num + 2:])
                break
            header = line[:line.index(':')]
            value = line[line.index(':') + 1:].strip()
            headers[header] = value
        return HttpResponse(status_code=int(status_code),
                            headers=headers,
                            body=body,
                            version=version)
