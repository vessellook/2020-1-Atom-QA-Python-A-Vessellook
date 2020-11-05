#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HttpRequest:
    method: str
    location: str
    headers: Optional[dict] = field(default_factory=dict)
    body: Optional[str] = None
    version: str = '1.0'

    def __repr__(self):
        request = f'{self.method} {self.location} HTTP/{self.version}\n'
        if self.body is not None:
            self.headers['Content-Length'] = len(self.body.encode(encoding='UTF-8'))
        request += '\n'.join([f'{header}: {value}' for header, value in self.headers])
        request += '\n\n'
        if self.body is not None:
            request += self.body
        return request

    def __bytes__(self):
        return str(self).encode(encoding='UTF-8')
