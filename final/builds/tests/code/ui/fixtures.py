import random
import time

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from settings import Settings
from ui.pages.registration_page import RegistrationPage
from ui.pages.authorization_page import AuthorizationPage


def enable_video(request: FixtureRequest, settings: Settings, name):
    def save():
        for i in range(60):
            try:
                open(f'{settings.video_dir}/{name}', 'rb')  # noqa
                break
            except FileNotFoundError:
                time.sleep(1)
        allure.attach.file(f'{settings.video_dir}/{name}',
                           attachment_type=allure.attachment_type.MP4)

    request.addfinalizer(save)


@pytest.fixture(scope='function')
def driver(request: FixtureRequest, settings: Settings):
    capabilities = {'acceptInsecureCerts': True}
    for mark in request.node.own_markers:
        if mark.name == 'enable_video' and settings.video_enable:
            capabilities['enableVideo'] = True
            name = f'{time.time()}_{random.random()}.mp4'
            capabilities['videoName'] = name
            enable_video(request, settings, name)
    driver = webdriver.Remote(command_executor=f'http://{settings.selenoid_netloc}/wd/hub',
                              options=ChromeOptions(),
                              desired_capabilities=capabilities)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def registration_page(driver):
    page = RegistrationPage(driver)
    page.make_request()
    return page


@pytest.fixture(scope='function')
def authorization_page(driver):
    page = AuthorizationPage(driver)
    page.make_request()
    return page
