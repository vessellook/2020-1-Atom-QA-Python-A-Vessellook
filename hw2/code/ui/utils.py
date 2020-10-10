import time
import random
from string import ascii_lowercase, ascii_uppercase


def generate_campaign_name(prefix='Кампания'):
    return f'{prefix} {time.time()} {random.random()}'


def lowercase_xpath(value: str):
    lowercase = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + ascii_lowercase
    uppercase = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + ascii_uppercase
    return f'translate({value},"{uppercase}","{lowercase}")'
