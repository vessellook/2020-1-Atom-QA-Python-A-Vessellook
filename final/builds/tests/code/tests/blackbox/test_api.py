"""Tests for myapp API functions, that only compare expected and real status codes"""
import allure
import pytest
import requests
# This function works as operator assert but not stop execution
import pytest_check as check

from clients.api_client import ApiClient
from utils import status_codes


def test_status(api_client: ApiClient):
    response = api_client.get_status()
    check.equal(response.status_code, status_codes.OK)
    check.equal(response.headers['Content-Type'], 'application/json')
    check.equal(response.json()['status'], 'ok')


class TestAdd:
    """Tests for add_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password', 'code'], [
        pytest.param("uZ5iwv9mHRau2XwUyq", "O0pUmj65FwBK5@BEX4B0Ic304jp.Jn_X",
                     "_nPnV9OXAUv4BRd8u4x", 201,
                     id="status code 210 instead of 201 [1]"),
        pytest.param("lgsI2JTTROPy", "ufA0AAb93mU@GgKg5eAlDqAF7y.jVdX", "c1oGe2lpHykxh", 201,
                     id="status code 210 instead of 201 [2]"),
        pytest.param("SxXkQphZlyU", "Nt_2EANGatP@corp.mail.ru", "k7p4abS9pz8", 201,
                     id="status code 210 instead of 201 [3]"),
        pytest.param("gqXyqCeSI0w1", "UPFHrwnm0zW@xvA42DyVVy1C.e7I", "", 400, id="empty password"),
        pytest.param("yzBG6H3WRK", "", "TOVZLrBqyRptj", 400, id="empty email"),
        pytest.param("", "xUGaUS3O7CmHN8@XfKKNxIWC4Fd5nwW0LJB.L9c", "g6PPzw2xHlXegUuBx_", 400,
                     id="empty username"),
        pytest.param("yqhhhkehDedxjl9ZQxEi", "SY59UhV1WLoPhZ_Vum0P@", "j8VUpXNfyRcbe", 400,
                     id="email without domain"),
        pytest.param("Ye4vpas2Y6a", "@hzJXSrXs5xtItIe.fhY", "JAY853ARpOLTkx", 400,
                     id="email without login"),
        pytest.param("8n62dfjLa69XPR2jH", "9tljbbnWGrOLr7.ru", "le0jpElLZ_", 400,
                     id="email without login@"),
        pytest.param("Ra1FY27beHOW9Ygbbys", "bpnjHs9xoyV@.ru", "RENDh9m1Hu65A", 400,
                     id="email with invalid domain"),
        pytest.param("JfBwfuSmYcloJ3", "sAzYuPLOv1QUz9PBe@mail.", "O42CXEz7oCq", 400,
                     id="invalid email domain"),
        pytest.param("8ox9fBbedjaWFQUS8sP", "oAvzOXnZJkQ82", "bA0PyaohHlhW9LS", 400,
                     id="invalid email")])
    def test_valid_json(self, username, email, password, code,
                        api_client: ApiClient):
        """Passes different auth_data (valid or invalid) to app with valid json"""
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == code

    @pytest.mark.API
    @pytest.mark.parametrize(['json', 'code'], [
        ({}, 400), ({'username': 'JmJ46wL1CgObdlYZfY'}, 400),
        ({'email': 'CcO2hP0pccOTDGyBOi@O56LMJgwOyrtO.wzGz'}, 400),
        ({'password': 'SlyVs9BNtXVcd3NyC'}, 400),
        ({'username': 'B2kthWKJSZa2m',
          'email': 'R8VfWkQncDCg4CzTElp3@sSZcFnRcm7uyoiwcE3z.ltFu9'}, 400),
        ({'username': 'AKsgVG9GXPcvxPQOzkDH', 'password': 'iFoe4A65FZ1'}, 400),
        ({'email': 'nHsv74vKecBib0Zfz@7GLvNEU4xAQ.dPNsf',
          'password': 'vUCyRJ6W70Q9EoADN_'}, 400),
        pytest.param({'username': -5, 'password': False, 'email': []}, 400,
                     id='210 status code instead of 400'),
        ([], 400),
        (['not', 'empty', 'list'], 400),
        ('just string', 400)
    ])
    def test_invalid_json(self, json, code, api_client: ApiClient):
        """Passes different invalid messages in json"""
        with allure.step('Send invalid json to add user'):
            response = requests.post(f'http://{api_client.netloc}/api/add_user',
                                     cookies=api_client.cookies,
                                     headers=api_client.headers,
                                     json=json)
            assert response.status_code == code


class TestDel:
    """Tests for del_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("jXlBnTbc5gpiz9iMy", "ye2YVs9cHG45@tKYxoKA_8VlwZxA.Cd0D1", "ooNkWYnmo5qFF_"),
        pytest.param("FiAkvDxsjCx", "UdXeLmsauBY3@UZw9bEbYbZPSldSoS.0qw5S", "9Yl4hp5_Zn4KQHE7D"),
        pytest.param("DAPKr0XEW1", "4F6Dbz7uaxnK@corp.mail.ru", "RKpZTwTMoXXCyNMl"),
        pytest.param("bWRp_WCZekujTS", "h3rqt_Zt8eld1@IhNo17B0f7U6p.QI_",
                     "bIKc98EZCZjqCBDBJ1v0' or 1 = 1 '; DROP DATABASE; --",
                     id="sql injection in password"),
    ])
    def test_added_users(self, username, email, password, api_client: ApiClient):
        """Add and delete users

        Passes different auth_data (valid or invalid) to app with valid json.
        If app accept to add user it tries to delete this user"""
        response = api_client.add_user(username=username, email=email, password=password)
        if response.status_code not in range(200, 300):
            pytest.skip('there were error with add_user function')
        with allure.step('Del user'):
            response2 = api_client.del_user(username)
            assert response2.status_code == status_codes.DELETED
        with allure.step('Del user again'):
            response3 = api_client.del_user(username)
            assert response3.status_code == status_codes.NOT_EXIST


class TestBlock:
    """Tests for block_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("oleVPFC4MrSJ5M2a4ty", "qtfmQG0TlMdqlZi2@ffsLCGnpVdH.3K0p", "Wf8bAkMOEPBngn"),
        pytest.param("2URYaA7ebE", "64AIR1LVJjJ_CEpbIR@YnUbudscDZzHQ.qx_wK", "S83adQxS6jGltbzR0w"),
        pytest.param("PLKapvmJTRpKerTsh", "PCzaRwYlMitt8@corp.mail.ru", "40GJGhVClBLO69DctqQ"),
        pytest.param("AnRY07pepWosuWi9", "IH1Jsht9U6e60MJpNNs@czwPpmi0HNHzPETQ.0vQj1",
                     "yQMmMzi6MAjLN' or 1 = 1 '; DROP DATABASE; --",
                     id="sql injection in password"),
    ])
    def test_added_users(self, username, email, password, api_client: ApiClient):
        """Add and delete users

        Passes different auth_data (valid or invalid) to app with valid json.
        If app accept to add user it tries to delete this user"""
        response = api_client.add_user(username=username, email=email, password=password)
        if response.status_code not in range(200, 300):
            pytest.skip('there were error with add_user function')
        with allure.step('Block user'):
            response2 = api_client.block_user(username)
            assert response2.status_code == status_codes.OK
        with allure.step('Block user again'):
            response3 = api_client.block_user(username)
            assert response3.status_code == status_codes.NOT_CHANGED


class TestAccept:
    """Tests for accept_user API function"""

    @pytest.mark.API
    @pytest.mark.parametrize(['username', 'email', 'password'], [
        pytest.param("W5bezo0pLs", "fH899uQfEQ6Gm6w@vmQJERazZPaT7yIprOVr.dUu", "3dFu4irYDL"),
        pytest.param("R_4uFz3zDYO2Y", "fq69Dfjhw9MJXfc@FpGgyxUfKqd.b6Nv", "wnCf0CvS1oibfY_N"),
        pytest.param("lM_9nXk6FC8eCDdu", "oS8sXS3iQDWB7lQf@corp.mail.ru", "in4NMj2A_OFxMkA"),
        pytest.param("sHctkbP27IiZFR", "c0bmefgdcajxiL22kD_@yS_jK_k0ZoX5K7r.wNtP",
                     "tXJL1_dD60TvUUC_6ksp' or 1 = 1 '; DROP DATABASE; --",
                     id="sql injection in password")
    ])
    def test_added_users(self, username, email, password, api_client: ApiClient):
        """Add and delete users

        Passes different auth_data (valid or invalid) to app with valid json.
        If app accept to add user it tries to delete this user"""
        response = api_client.add_user(username=username, email=email, password=password)
        if response.status_code not in range(200, 300):
            pytest.skip('there were error with add_user function')
        with allure.step('Accept user again'):
            response2 = api_client.accept_user(username)
            assert response2.status_code == status_codes.NOT_CHANGED
        with allure.step('Block user and accept him'):
            response3 = api_client.block_user(username)
            response4 = api_client.accept_user(username)
            assert response4.status_code == status_codes.OK
        with allure.step('Accept user again'):
            response5 = api_client.accept_user(username)
            assert response5.status_code == status_codes.NOT_CHANGED


@pytest.mark.scenario
@pytest.mark.API
def test_scenario(api_client: ApiClient):
    """Test with several requests"""

    username = 'my-username'
    email = 'my-email@gmail.com'
    password = 'I love eating pizza'

    with allure.step(f"Del user {username} who doesn't exist"):
        response = api_client.del_user(username)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f"Block user {username} who doesn't exist"):
        response = api_client.block_user(username)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f"Accept user {username} who doesn't exist"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.NOT_EXIST
    with allure.step(f'Add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == status_codes.CREATED
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Block user {username}"):
        response = api_client.block_user(username)
        assert response.status_code == status_codes.OK
    with allure.step(f"Block user {username} again"):
        response = api_client.block_user(username)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.OK
    with allure.step(f"Accept user {username}"):
        response = api_client.accept_user(username)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f"Del user {username}"):
        response = api_client.del_user(username)
        assert response.status_code == status_codes.DELETED
    with allure.step(f'Add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == status_codes.CREATED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email=email, password=password)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username=username, email='a' + email, password=password)
        assert response.status_code == status_codes.NOT_CHANGED
    with allure.step(f'Try to add user with credentials ({username}, {email}, {password})'):
        response = api_client.add_user(username='a' + username, email=email, password=password)
        assert response.status_code == status_codes.NOT_CHANGED
