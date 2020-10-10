import pytest
from ui.pages.main_page import MainPage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.segments_page import SegmentsPage

from ui.utils import generate_campaign_name, generate_segment_name


@pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_main_title(main_page: MainPage):
    assert main_page.get_title() == 'Рекламная платформа myTarget — Сервис таргетированной рекламы'


@pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_auth(dashboard_page: DashboardPage):
    assert dashboard_page.is_url_matches()


@pytest.mark.skip(reason="It's working fine")
@pytest.mark.UI
def test_create_campaign(create_campaign_page: CreateCampaignPage):
    assert create_campaign_page.is_url_matches()


@pytest.mark.skip(reason="no need")
@pytest.mark.UI
@pytest.mark.parametrize("post_url", ['https://ok.ru/bonapp/topic/152072476224923',
                                      'http://ok.ru/bonapp/topic/152081249463707',
                                      'ok.ru/bonapp/topic/152080570707355'])
def test_create_vk_post_campaign(create_campaign_page: CreateCampaignPage, post_url):
    campaign_name = generate_campaign_name()
    create_campaign_page.social_engagement(post_url, campaign_name, 500, 10000)


@pytest.mark.skip
@pytest.mark.UI
# @pytest.mark.parametrize("site_url", ['https://vk.com', 'vk.com', 'site-does-not-exist.ru'])
@pytest.mark.parametrize("site_url", ['https://vk.com'])
def test_create_site_traffic_campaign(create_campaign_page: CreateCampaignPage, site_url):
    campaign_name = generate_campaign_name()
    dashboard_page: DashboardPage = create_campaign_page.traffic(site_url, campaign_name, 500, 10000)
    assert dashboard_page.has_campaign(campaign_name)
    dashboard_page.remove_campaign(campaign_name)
    assert not dashboard_page.has_campaign(campaign_name)


# @pytest.mark.skip
@pytest.mark.UI
def test_create_segment(segments_page: SegmentsPage):
    segment_name = generate_segment_name()
    segments_page.create_segment(segment_name)
    assert segments_page.has_segment(segment_name)
    segments_page.remove_segment(segment_name)
    assert not segments_page.has_segment(segment_name)
