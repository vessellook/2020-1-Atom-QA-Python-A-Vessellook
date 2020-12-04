"""This file provides some short functions to generate unique objects"""
import random
from time import time
from string import ascii_letters, digits


def string(alphabet=ascii_letters + digits, min_len=6, max_len=16):
    return ''.join([random.choice(alphabet) for i in range(random.randint(min_len, max_len))])


def integer():
    return time() + random.random() * 1000000


def email(login: str = None, domain: str = None):
    login = login if login is not None else string(max_len=7)
    domain = domain if domain is not None else f'{string(max_len=7)}' \
                                               f'.{string(min_len=1, max_len=4)}{random.choice(ascii_letters)}'
    return f'{login}@{domain}'


_email = email


def auth_data(username: str = None, email: str = None, password: str = None):  # noqa: disable=W0621
    username = username if username is not None else string()
    email = email if email is not None else _email()  # noqa: disable=W0621
    password = password if password is not None else string()
    print('auth_data:', username, email, password)
    return username, email, password
