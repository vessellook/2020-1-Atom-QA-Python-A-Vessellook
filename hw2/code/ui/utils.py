import time
import random
from string import ascii_lowercase, ascii_uppercase
from selenium.webdriver.common.by import By
from typing import Tuple


def generate_campaign_name(prefix='Кампания'):
    return f'{prefix} {time.time()} {random.random()}'


def generate_segment_name(prefix='Сегмент'):
    return f'{prefix} {time.time()} {random.random()}'


def lowercase_xpath(value: str):
    lowercase = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + ascii_lowercase
    uppercase = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + ascii_uppercase
    return f'translate({value},"{uppercase}","{lowercase}")'


def _form_attribute(attribute: str, value: str, strict_match: bool = False):
    if attribute[0] != '@':
        attribute = '@' + attribute

    if strict_match:
        return f'{attribute}="{value}"'
    else:
        return f'contains({attribute},"{value}")'


class XPATH:
    def __init__(self, tag: str = '*'):
        self.xpath = tag

    def __str__(self):
        return f'//{self.xpath}'

    @staticmethod
    def lowercase(value: str):
        lowercase = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + ascii_lowercase
        uppercase = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' + ascii_uppercase
        return f'translate({value},"{uppercase}","{lowercase}")'

    def _add(self, xpath_part: str):
        """Helper method to prevent bugs tied with mistyping '=' instead of '+='"""
        self.xpath += xpath_part

    def disallow_class(self, classname: str):
        self._add(f'[not({_form_attribute(attribute="class", value=classname, strict_match=False)})]')
        return self

    def add_class(self, classname: str):
        return self.add_attribute(attribute='class', value=classname, strict_match=False)

    def add_attribute(self, attribute: str, value: str, strict_match: bool = False):
        self._add(f'[{_form_attribute(attribute, value, strict_match)}]')
        return self

    def add_num(self, num: int):
        self._add(f'[{num}]')
        return self

    def add_predicate(self, predicate: str):
        if predicate[0] != '[':
            self._add(f'[{predicate}]')
        else:
            self._add(predicate)
        return self

    def add_descendant(self, descendant: str = '*'):
        self._add(f'//{descendant}')
        return self

    def add_parent(self, parent: str = '*'):
        if 'parent::' not in parent:
            parent = 'parent::' + parent
        self._add(f'/{parent}')
        return self

    def add_following_sibling(self, sibling: str = '*'):
        if 'following-sibling::' not in sibling:
            sibling = 'following-sibling::' + sibling
        self._add(f'/{sibling}')
        return self


def locator(xpath: XPATH) -> Tuple[By, str]:
    if xpath.__class__ == XPATH:
        return By.XPATH, str(xpath)
