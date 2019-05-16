import pytest
import base64
import json

from requests import Response

from py42._internal.session import Py42Session
from py42._internal.login_providers import BasicAuthProvider, C42ApiV1TokenProvider, C42ApiV3TokenProvider,\
    C42APILoginTokenProvider, C42APIStorageAuthTokenProvider, FileEventLoginProvider

from tests.shared_test_utils import successful_request, MockPy42Session

USERNAME = "username"
PASSWORD = "password"
HOST_ADDRESS = "https://test.code42.com"

V1_TOKEN_PART1 = "partone"
V1_TOKEN_PART2 = "parttwo"

V3_TOKEN = "v3usertokenstring"

TMP_LOGIN_TOKEN = "tmplogintokenstring"
STORAGE_HOST_ADDRESS = "https://testsstorage.code42.com"

NODE_GUID = "nodeguid"

STS_BASE_URL = "https://sts-east.us.code42.com"

SERVER_ENV_EXCEPTION_MESSAGE = "Internal error in /api/ServerEnv"


@successful_request
def v1_auth_token_request_handler(response):
    response._content = json.dumps({"data": [V1_TOKEN_PART1, V1_TOKEN_PART2]})
    return response


@successful_request
def v3_auth_token_request_handler(response):
    response._content = json.dumps({"data": {"v3_user_token": V3_TOKEN}})
    return response


@successful_request
def tmp_login_token_request_handler(response):
    response._content = json.dumps({"data": {"loginToken": TMP_LOGIN_TOKEN, "serverUrl": STORAGE_HOST_ADDRESS}})
    return response


@pytest.fixture(scope="module")
def v1_auth_provider():
    auth_session = MockPy42Session(HOST_ADDRESS, request_handler=v1_auth_token_request_handler)
    provider = C42ApiV1TokenProvider(auth_session)
    return provider


@pytest.fixture(scope="module")
def v3_auth_provider():
    auth_session = MockPy42Session(HOST_ADDRESS, request_handler=v3_auth_token_request_handler)
    provider = C42ApiV3TokenProvider(auth_session)
    return provider


@pytest.fixture
def login_token_provider():
    auth_session = MockPy42Session(HOST_ADDRESS, request_handler=tmp_login_token_request_handler)
    provider = C42APILoginTokenProvider(auth_session, "my", "device-guid", "destination-guid")
    return provider


@pytest.fixture
def storage_auth_token_provider():
    auth_session = MockPy42Session(HOST_ADDRESS, request_handler=tmp_login_token_request_handler)
    provider = C42APIStorageAuthTokenProvider(auth_session, "plan-id", "destination-guid", node_guid=NODE_GUID)
    return provider


@pytest.fixture
def file_event_login_provider_with_sts(mocker):
    auth_session = mocker.MagicMock(spec=Py42Session)

    def mock_get(uri, **kwargs):
        if uri == "/api/ServerEnv":
            response = mocker.MagicMock(spec=Response)
            response.content = json.dumps({"stsBaseUrl": STS_BASE_URL})
            response.status_code = 200
        elif uri == "/c42api/v3/auth/jwt":
            response = mocker.MagicMock(spec=Response)
            response.content = json.dumps({"data": {"v3_user_token": V3_TOKEN}})
            response.status_code = 200
        return response

    auth_session.get.side_effect = mock_get
    return FileEventLoginProvider(auth_session)


@pytest.fixture
def file_event_login_provider_no_sts(mocker):
    auth_session = mocker.MagicMock(spec=Py42Session)

    def mock_get(uri, **kwargs):
        response = mocker.MagicMock(spec=Response)
        response.content = json.dumps({})
        response.status_code = 200
        return response

    auth_session.get.side_effect = mock_get
    return FileEventLoginProvider(auth_session)


@pytest.fixture
def file_event_login_provider_server_env_exception(mocker):
    auth_session = mocker.MagicMock(spec=Py42Session)

    def mock_get(uri, **kwargs):
        raise Exception(SERVER_ENV_EXCEPTION_MESSAGE)

    auth_session.get.side_effect = mock_get
    return FileEventLoginProvider(auth_session)


@pytest.fixture(scope="module")
def basic_auth_provider():
    return BasicAuthProvider(HOST_ADDRESS, USERNAME, PASSWORD)


def test_basic_provider_constructs_successfully():
    assert BasicAuthProvider(HOST_ADDRESS, USERNAME, PASSWORD)


def test_basic_provider_secret_returns_base64_credentials(basic_auth_provider):
    # type: (BasicAuthProvider) -> None

    expected_credentials = "{0}:{1}".format(USERNAME, PASSWORD)
    expected_b64_credentials = base64.encodestring(expected_credentials).replace("\n", "")

    provider_credentials = basic_auth_provider.get_secret_value()

    assert provider_credentials == expected_b64_credentials


def test_basic_provider_host_address_matches_supplied(basic_auth_provider):
    # type: (BasicAuthProvider) -> None
    assert basic_auth_provider.get_target_host_address() == HOST_ADDRESS


def test_v1_auth_provider_constructs_successfully():
    assert C42ApiV1TokenProvider(MockPy42Session(HOST_ADDRESS))


def test_v1_auth_provider_host_address_matches_supplied(v1_auth_provider):
    assert v1_auth_provider.get_target_host_address() == HOST_ADDRESS


def test_v1_auth_provider_secret_returns_v1_token(v1_auth_provider):
    # type: (C42ApiV1TokenProvider) -> None
    assert v1_auth_provider.get_secret_value() == "{0}-{1}".format(V1_TOKEN_PART1, V1_TOKEN_PART2)


def test_v3_auth_provider_constructs_successfully():
    assert C42ApiV3TokenProvider(MockPy42Session(HOST_ADDRESS))


def test_v3_auth_provider_host_address_matches_supplied(v3_auth_provider):
    # type: (C42ApiV3TokenProvider) -> None
    assert v3_auth_provider.get_target_host_address() == HOST_ADDRESS


def test_v3_auth_provider_secret_returns_v3_token(v3_auth_provider):
    # type: (C42ApiV3TokenProvider) -> None
    assert v3_auth_provider.get_secret_value() == V3_TOKEN


def test_login_token_provider_constructs_successfully():
    assert C42APILoginTokenProvider(MockPy42Session(HOST_ADDRESS), "my", "device-guid", "destination-guid")


def test_login_token_provider_host_address_returns_storage_url(login_token_provider):
    # type: (C42APILoginTokenProvider) -> None
    assert login_token_provider.get_target_host_address() == STORAGE_HOST_ADDRESS


def test_login_token_provider_secret_returns_tmp_login_token(login_token_provider):
    # type: (C42APILoginTokenProvider) -> None
    assert login_token_provider.get_secret_value() == TMP_LOGIN_TOKEN


def test_storage_auth_token_provider_constructs_successfully():
    assert C42APIStorageAuthTokenProvider(MockPy42Session(HOST_ADDRESS), "plan-id", "destination-guid",
                                          node_guid=NODE_GUID)


def test_storage_auth_token_provider_host_address_returns_storage_url(storage_auth_token_provider):
    # type: (C42APIStorageAuthTokenProvider) -> None
    assert storage_auth_token_provider.get_target_host_address() == STORAGE_HOST_ADDRESS


def test_storage_auth_token_provider_returns_tmp_login_token(storage_auth_token_provider):
    # type: (C42APIStorageAuthTokenProvider) -> None
    assert storage_auth_token_provider.get_secret_value() == TMP_LOGIN_TOKEN


def test_storage_auth_token_provider_node_guid_matches_supplied(storage_auth_token_provider):
    # type: (C42APIStorageAuthTokenProvider) -> None
    assert storage_auth_token_provider.node_guid == NODE_GUID


class TestFileEventLoginProvider(object):

    def test_get_target_host_address_given_sts_base_url_returns_fs_base_url(self, file_event_login_provider_with_sts):
        host_address = file_event_login_provider_with_sts.get_target_host_address()
        assert host_address == "https://forensicsearch-east.us.code42.com"

    def test_get_target_host_address_given_no_sts_base_url_raises_exception(self, file_event_login_provider_no_sts):
        with pytest.raises(Exception) as e:
            file_event_login_provider_no_sts.get_target_host_address()
        expected_message = "stsBaseUrl not found. Cannot determine file event service host address."
        assert e.value.args[0] == expected_message

    def test_get_target_host_address_given_exception_retrieving_server_env_raises_exception(self,
                                                                        file_event_login_provider_server_env_exception):
        with pytest.raises(Exception) as e:
            file_event_login_provider_server_env_exception.get_target_host_address()
        expected_message = "An error occurred while requesting server environment information, caused by {0}"\
            .format(SERVER_ENV_EXCEPTION_MESSAGE)
        assert e.value.args[0] == expected_message

    def test_get_secret_value_given_auth_session_returns_v3_token(self, file_event_login_provider_with_sts):
        secret = file_event_login_provider_with_sts.get_secret_value()
        assert secret == V3_TOKEN


@pytest.mark.parametrize("tmp_token_provider", ["login_token_provider", "storage_auth_token_provider"],
                         ids=["login_token_provider", "storage_auth_token_provider"])
def test_tmp_token_provider_uses_cache_after_get_target_host_address_called(tmp_token_provider, request, mocker):
    tmp_token_provider = request.getfixturevalue(tmp_token_provider)
    mocker.spy(tmp_token_provider, 'get_tmp_auth_token')
    tmp_token_provider.get_target_host_address()
    assert tmp_token_provider.get_tmp_auth_token.call_count == 1, "get_tmp_auth_token never called"
    tmp_token_provider.get_target_host_address()
    tmp_token_provider.get_secret_value()

    call_count = tmp_token_provider.get_tmp_auth_token.call_count
    message = "get_tmp_auth_token was called {0} times, expected once".format(call_count)
    assert call_count == 1, message


@pytest.mark.parametrize("tmp_token_provider", ["login_token_provider", "storage_auth_token_provider"],
                         ids=["login_token_provider", "storage_auth_token_provider"])
def test_tmp_token_provider_uses_cache_after_get_secret_value_called(tmp_token_provider, request, mocker):
    tmp_token_provider = request.getfixturevalue(tmp_token_provider)
    mocker.spy(tmp_token_provider, 'get_tmp_auth_token')
    tmp_token_provider.get_secret_value()
    assert tmp_token_provider.get_tmp_auth_token.call_count == 1, "get_tmp_auth_token never called"
    tmp_token_provider.get_secret_value()
    tmp_token_provider.get_target_host_address()

    call_count = tmp_token_provider.get_tmp_auth_token.call_count
    message = "get_tmp_auth_token was called {0} times, expected once".format(call_count)
    assert call_count == 1, message
