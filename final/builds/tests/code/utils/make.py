"""This file provides some short functions to generate unique objects"""
import random
from time import time
from string import ascii_letters, digits


def string(alphabet=ascii_letters + digits, min_len=6, max_len=16):
    return ''.join([random.choice(alphabet) for i in range(random.randint(min_len, max_len))])


def integer():
    return time() + random.random() * 1000000


def email(login: str = None, domain: str = None):
    if login is None:
        login = string(max_len=7)
    if domain is None:
        domain = f'{string(max_len=7)}.{string(min_len=1, max_len=4)}{random.choice(ascii_letters)}'
    return f'{login}@{domain}'


_email = email


def auth_data(username: str = None, email: str = None, password: str = None):  # noqa: disable=W0621
    if username is None:
        username = string()
    if email is None:
        email = _email()  # noqa: disable=W0621
    if password is None:
        password = string()
    return username, email, password
