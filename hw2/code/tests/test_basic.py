import pytest
import allure
from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.segments_page import SegmentsPage
from variables import EMAIL, PASSWORD

from ui.utils import generate_campaign_name, generate_segment_name


# @pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_main_title(main_page: MainPage):
    assert main_page.get_title() == 'Рекламная платформа myTarget — Сервис таргетированной рекламы'


# @pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_auth(main_page: MainPage):
    with allure.step('Auth to target.my.com'):
        dashboard_page = main_page.auth(EMAIL, PASSWORD)
    assert dashboard_page.is_url_matches('target.my.com/dashboard')


# @pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
@pytest.mark.parametrize('email, password', [('email-invalid', 'some-password')])
def test_auth_negative(main_page: MainPage, email, password):
    with allure.step(f'Auth with wrong credentials {email, password} to target.my.com'):
        not_dashboard_page = main_page.auth(email, password)
    assert not not_dashboard_page.is_url_matches('target.my.com/dashboard')


# @pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_create_campaign(dashboard_page: DashboardPage):
    with allure.step(f'Open CreateCampaignPage'):
        create_campaign_page = dashboard_page.create_campaign()
    assert create_campaign_page.is_url_matches()


# @pytest.mark.skip(reason="no need")
# @pytest.mark.UI
# @pytest.mark.parametrize("post_url", ['https://ok.ru/bonapp/topic/152072476224923',
#                                       'http://ok.ru/bonapp/topic/152081249463707',
#                                       'ok.ru/bonapp/topic/152080570707355'])
# def test_create_vk_post_campaign(create_campaign_page: CreateCampaignPage, post_url):
#     campaign_name = generate_campaign_name()
#     create_campaign_page.social_engagement(post_url, campaign_name, 500, 10000)


# @pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
@pytest.mark.parametrize('site_url', ['https://vk.com', 'vk.com', 'site-does-not-exist.ru'])
# @pytest.mark.parametrize('site_url', ['https://vk.com'])
def test_create_site_traffic_campaign(create_campaign_page: CreateCampaignPage, site_url):
    campaign_name = generate_campaign_name()
    with allure.step(f'create campaign with name {campaign_name}'):
        dashboard_page = create_campaign_page.traffic(site_url, campaign_name, 500, 10000)
    dashboard_page.refresh()
    assert dashboard_page.has_campaign(campaign_name)
    with allure.step(f'remove campaign with name {campaign_name}'):
        dashboard_page.remove_campaign(campaign_name)
    dashboard_page.refresh()
    assert not dashboard_page.has_campaign(campaign_name)


# @pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_create_segment(segments_page: SegmentsPage):
    segment_name = generate_segment_name()
    with allure.step(f'create segment with name {segments_page}'):
        segments_page.create_segment(segment_name)
    assert segments_page.has_segment(segment_name)
    with allure.step(f'remove segment with name {segments_page}'):
        segments_page.remove_segment(segment_name)
    segments_page.refresh()
    assert not segments_page.has_segment(segment_name)
