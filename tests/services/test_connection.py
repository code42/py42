import pytest
from requests import Response
from tests.conftest import TEST_DEVICE_GUID

import pycpg.settings as settings
from pycpg.exceptions import PycpgDeviceNotConnectedError
from pycpg.exceptions import PycpgError
from pycpg.exceptions import PycpgFeatureUnavailableError
from pycpg.exceptions import PycpgInternalServerError
from pycpg.exceptions import PycpgUnauthorizedError
from pycpg.response import PycpgResponse
from pycpg.services._auth import CPGRenewableAuth
from pycpg.services._connection import ConnectedServerHostResolver
from pycpg.services._connection import Connection
from pycpg.services._connection import HostResolver
from pycpg.services._connection import KnownUrlHostResolver
from pycpg.services._connection import MicroserviceKeyHostResolver
from pycpg.services._connection import MicroservicePrefixHostResolver
from pycpg.services._keyvaluestore import KeyValueStoreService

default_kwargs = {
    "timeout": 60,
    "proxies": None,
    "stream": False,
    "verify": True,
    "cert": None,
}
HOST_ADDRESS = "http://example.com"
URL = "/api/resource"
DATA_VALUE = '{"test": "data"}'
JSON_VALUE = {"key": "value"}
KWARGS_INDEX = 1
DATA_KEY = "data"
TEST_RESPONSE_CONTENT = '{"key": "test_response_content"}'


@pytest.fixture
def mock_host_resolver(mocker):
    mock = mocker.MagicMock(spec=HostResolver)
    mock.get_host_address.return_value = HOST_ADDRESS
    return mock


@pytest.fixture
def mock_auth(mocker):
    return mocker.MagicMock(spec=CPGRenewableAuth)


@pytest.fixture
def mock_key_value_service(mocker):
    return mocker.MagicMock(spec=KeyValueStoreService)


@pytest.fixture
def mock_server_env_conn(mocker):
    mock_conn = mocker.MagicMock(spec=Connection)
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = '{"stsBaseUrl": "sts-testsuffix"}'
    mock_conn.get.return_value = PycpgResponse(mock_response)
    return mock_conn


@pytest.fixture
def mock_server_env_conn_missing_sts_base_url(mocker):
    mock_conn = mocker.MagicMock(spec=Connection)
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = "{}"
    mock_conn.get.return_value = PycpgResponse(mock_response)
    return mock_conn


@pytest.fixture
def mock_connected_server_conn(mocker):
    mock_conn = mocker.MagicMock(spec=Connection)
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = f'{{"serverUrl": "{HOST_ADDRESS}"}}'
    mock_conn.get.return_value = PycpgResponse(mock_response)
    return mock_conn


@pytest.fixture
def mock_not_connected_server_conn(mocker):
    mock_conn = mocker.MagicMock(spec=Connection)
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = '{"serverUrl": null}'
    mock_conn.get.return_value = PycpgResponse(mock_response)
    return mock_conn


@pytest.fixture
def proxy_set():
    settings.proxies = {"https": "http://localhost:9999"}
    yield
    settings.proxies = None


class MockPreparedRequest:
    def __init__(self, method, url, data=None, json=None):
        self._method = method
        self._url = url
        self._data = data or []
        self._json = json or {}

    def __eq__(self, other):
        return (
            self._method == other.method
            and self._url == other.url
            and self._data == other.data
        )


class TestKnownUrlHostResolver:
    def test_get_host_address_returns_expected_value(self):
        resolver = KnownUrlHostResolver(HOST_ADDRESS)
        assert resolver.get_host_address() == HOST_ADDRESS


class TestMicroserviceKeyHostResolver:
    def test_get_host_address_returns_expected_value(self, mock_key_value_service):
        mock_key_value_service.get_stored_value.return_value.text = HOST_ADDRESS
        resolver = MicroserviceKeyHostResolver(mock_key_value_service, "TEST_KEY")
        assert resolver.get_host_address() == HOST_ADDRESS

    def test_get_host_address_passes_expected_key(self, mock_key_value_service):
        resolver = MicroserviceKeyHostResolver(mock_key_value_service, "TEST_KEY")
        resolver.get_host_address()
        mock_key_value_service.get_stored_value.assert_called_once_with("TEST_KEY")


class TestMicroservicePrefixHostResolver:
    def test_get_host_address_returns_expected_value(self, mock_server_env_conn):
        resolver = MicroservicePrefixHostResolver(mock_server_env_conn, "TESTPREFIX")
        assert resolver.get_host_address() == "TESTPREFIX-testsuffix"

    def test_get_host_address_when_sts_base_url_not_found_raises_feature_unavailable_error(
        self, mock_server_env_conn_missing_sts_base_url
    ):
        resolver = MicroservicePrefixHostResolver(
            mock_server_env_conn_missing_sts_base_url, "TESTPREFIX"
        )
        with pytest.raises(PycpgFeatureUnavailableError):
            resolver.get_host_address()

    def test_get_host_address_calls_correct_server_env_url(self, mock_server_env_conn):
        resolver = MicroservicePrefixHostResolver(mock_server_env_conn, "TESTPREFIX")
        resolver.get_host_address()
        mock_server_env_conn.get.assert_called_once_with("/api/v1/ServerEnv")


class TestConnectedServerHostResolver:
    def test_get_host_address_returns_expected_value(self, mock_connected_server_conn):
        resolver = ConnectedServerHostResolver(
            mock_connected_server_conn, TEST_DEVICE_GUID
        )
        actual = resolver.get_host_address()
        assert actual == HOST_ADDRESS
        mock_connected_server_conn.get.assert_called_once_with(
            "api/v1/connectedServerUrl", params={"guid": TEST_DEVICE_GUID}
        )

    def test_get_host_address_when_server_returns_none_raises_expected_error(
        self, mock_not_connected_server_conn
    ):
        resolver = ConnectedServerHostResolver(
            mock_not_connected_server_conn, TEST_DEVICE_GUID
        )
        with pytest.raises(PycpgDeviceNotConnectedError) as err:
            resolver.get_host_address()

        expected_message = (
            "Device with GUID 'device-guid' is not currently connected "
            "to the Authority server."
        )
        assert expected_message in str(err.value)
        assert err.value.device_guid == TEST_DEVICE_GUID


class TestConnection:
    def test_connection_get_calls_requests_with_get(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.get(URL)
        expected = MockPreparedRequest("GET", HOST_ADDRESS + URL)
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_put_calls_requests_with_put(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data=DATA_VALUE)
        expected = MockPreparedRequest(
            "PUT", HOST_ADDRESS + URL, data=DATA_VALUE.encode("utf-8")
        )
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_post_calls_requests_with_post(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.post(URL, data=DATA_VALUE)
        expected = MockPreparedRequest(
            "POST", HOST_ADDRESS + URL, data=DATA_VALUE.encode("utf-8")
        )
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_patch_calls_requests_with_patch(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.patch(URL, data=DATA_VALUE)
        expected = MockPreparedRequest(
            "PATCH", HOST_ADDRESS + URL, data=DATA_VALUE.encode("utf-8")
        )
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_delete_calls_requests_with_delete(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.delete(URL)
        expected = MockPreparedRequest("DELETE", HOST_ADDRESS + URL)
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_options_calls_requests_with_options(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.options(URL)
        expected = MockPreparedRequest("OPTIONS", HOST_ADDRESS + URL)
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_head_calls_requests_with_head(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.head(URL)
        expected = MockPreparedRequest("HEAD", HOST_ADDRESS + URL)
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_post_with_json_prepares_request_with_json(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.post(URL, json=JSON_VALUE)
        expected = MockPreparedRequest(
            "POST", HOST_ADDRESS + URL, data=None, json=JSON_VALUE
        )
        success_requests_session.prepare_request.assert_called_once_with(expected)

    def test_connection_request_returns_utf8_response(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        response = connection.request("GET", URL, data=DATA_VALUE, json=JSON_VALUE)
        assert response.encoding == "utf-8"

    def test_connection_request_when_streamed_doesnt_not_set_encoding_on_response(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        response = connection.request("GET", URL, data=DATA_VALUE, stream=True)
        assert response.encoding is None

    def test_connection_request_returns_response_when_good_status_code(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        response = connection.get(URL)
        assert response.text == TEST_RESPONSE_CONTENT

    def test_connection_request_with_error_status_code_raises_http_error(
        self, mock_host_resolver, mock_auth, error_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, error_requests_session)
        with pytest.raises(PycpgInternalServerError):
            connection.get(URL)

    def test_connection_request_calls_auth_handler_when_making_first_request(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.get(URL)
        assert success_requests_session.prepare_request.call_count == 1

    def test_connection_request_calls_auth_handler_clears_renews_credentials_when_response_unauthorized(
        self, mock_host_resolver, mock_auth, renewed_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, renewed_requests_session)
        connection.get(URL)
        assert renewed_requests_session.send.call_count == 2
        assert renewed_requests_session.prepare_request.call_count == 2
        assert mock_auth.clear_credentials.call_count == 1

    def test_connection_request_raises_unauthorized_error_when_renewal_results_in_401(
        self, mock_host_resolver, mock_auth, unauthorized_requests_session
    ):
        connection = Connection(
            mock_host_resolver, mock_auth, unauthorized_requests_session
        )

        with pytest.raises(PycpgUnauthorizedError):
            connection.get(URL)

        assert unauthorized_requests_session.send.call_count == 2

    def test_connection_request_when_session_returns_none_raises_pycpg_error(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        success_requests_session.send.return_value = None
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        with pytest.raises(PycpgError):
            connection.get(URL)

    def test_connection_request_when_no_data_does_not_include_content_type_header(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL)
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers.get("Content-Type") is None

    def test_connection_request_when_has_data_includes_content_type_header(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data='{"foo":"bar"}')
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers["Content-Type"] == "application/json"

    def test_connection_request_when_has_data_does_not_use_header_on_following_request_that_does_not_have_data(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data='{"foo":"bar"}')  # Content-Type: application/json
        connection.get(URL)
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers.get("Content-Type") is None

    def test_connection_request_uses_given_headers(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(
            URL, data='{"foo":"bar"}', headers={"Header1": "Foo", "Header2": "Bar"}
        )
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers["Header1"] == "Foo"
        assert request.headers["Header2"] == "Bar"

    def test_connection_request_when_given_header_as_param_does_not_persist_header(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data='{"foo":"bar"}', headers={"Foo": "Bar"})
        connection.get(URL)
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers.get("Foo") is None

    def test_connection_request_includes_user_agent_header(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL)
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers["User-Agent"] is not None

    def test_connection_request_is_able_to_accept_content_type_header(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data='{"foo":"bar"}', headers={"Content-Type": "*/*"})
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers["Content-Type"] == "*/*"

    def test_connection_request_is_able_to_accept_accept_header(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data='{"foo":"bar"}', headers={"Accept": "*/*"})
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers["Accept"] == "*/*"

    def test_connection_request_when_not_give_accept_header_sets_accept_to_application_json(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data='{"foo":"bar"}')
        request = success_requests_session.prepare_request.call_args[0][0]
        assert request.headers["Accept"] == "application/json"

    def test_connection_request_when_proxies_set_passes_proxies_arg_to_session_send(
        self, proxy_set, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(
            mock_host_resolver, mock_auth, session=success_requests_session
        )
        url = "https://example.com"
        connection.get(url)
        connection.post(url)
        connection.options(url)
        connection.put(url)
        connection.patch(url)
        connection.head(url)
        connection.delete(url)
        for call in success_requests_session.send.call_args_list:
            assert call[1]["proxies"] == {"https": "http://localhost:9999"}
