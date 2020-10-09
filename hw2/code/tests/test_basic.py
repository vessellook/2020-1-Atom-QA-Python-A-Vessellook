import pytest

from ui.pages.main_page import MainPage
from ui.pages.create_campaign_page import CreateCampaignPage
from ui.pages.dashboard_page import DashboardPage


@pytest.mark.UI
def test_main_title(main_page: MainPage):
    assert main_page.get_title() == 'Рекламная платформа myTarget — Сервис таргетированной рекламы'


@pytest.mark.UI
def test_auth(dashboard_page: DashboardPage):
    assert dashboard_page.is_url_matches()


@pytest.mark.UI
def test_create_campaign(create_campaign_page: CreateCampaignPage):
    assert create_campaign_page.is_url_matches()
