import json
from time import time


def jsonify(obj) -> bytes:
    return json.dumps(obj).encode()


def unjsonify(data: bytes):
    return json.loads(data)


def generate_token():
    return str(time())
