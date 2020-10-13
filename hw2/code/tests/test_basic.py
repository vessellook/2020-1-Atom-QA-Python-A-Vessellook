import pytest

from conftest import AuthFailedException
from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.segments_page import SegmentsPage
from variables import EMAIL, PASSWORD
from ui.utils import generate_campaign_name, generate_segment_name


@pytest.mark.UI
def test_main_title(main_page: MainPage):
    assert main_page.title == 'Рекламная платформа myTarget — Сервис таргетированной рекламы'


@pytest.mark.UI
def test_auth(main_page: MainPage):
    dashboard_page = main_page.auth(EMAIL, PASSWORD)
    assert 'target.my.com/dashboard' in dashboard_page.url


@pytest.mark.UI
@pytest.mark.parametrize('email, password', [
    ('email-invalid', 'some-password'),
    ('email@valid.com', 'password-invalid-i-hope'),
    (EMAIL, PASSWORD + '-wrong-password'),
    (str(), str()),
    ('admin', "' or 1 = 1 -- ")
])
def test_auth_negative(main_page: MainPage, email, password):
    with pytest.raises(AuthFailedException):
        main_page.auth(email, password)


@pytest.mark.UI
def test_create_campaign(dashboard_page: DashboardPage):
    create_campaign_page = dashboard_page.create_campaign()
    assert create_campaign_page.is_url_matches()


@pytest.mark.UI
@pytest.mark.parametrize('site_url', ['https://vk.com', 'vk.com', 'site-does-not-exist.ru'])
def test_create_site_traffic_campaign(create_campaign_page: CreateCampaignPage, site_url):
    campaign_name = generate_campaign_name()
    dashboard_page = create_campaign_page.traffic(site_url, campaign_name, 500, 10000)
    dashboard_page.refresh()
    assert dashboard_page.has_campaign(campaign_name)
    dashboard_page.remove_campaign(campaign_name)
    dashboard_page.refresh()
    assert not dashboard_page.has_campaign(campaign_name)


@pytest.mark.UI
def test_create_segment(segments_page: SegmentsPage):
    segment_name = generate_segment_name()
    segments_page.create_segment(segment_name)
    assert segments_page.has_segment(segment_name)
    segments_page.remove_segment(segment_name)
    segments_page.refresh()
    assert not segments_page.has_segment(segment_name)
