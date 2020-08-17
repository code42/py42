import json

import pytest
from requests import Response

from py42.exceptions import Py42Error
from py42.exceptions import Py42FeatureUnavailableError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42UnauthorizedError
from py42.response import Py42Response
from py42.services._auth import C42RenewableAuth
from py42.services._connection import Connection
from py42.services._connection import HostResolver
from py42.services._connection import KnownUrlHostResolver
from py42.services._connection import MicroserviceKeyHostResolver
from py42.services._connection import MicroservicePrefixHostResolver
from py42.services._keyvaluestore import KeyValueStoreClient

default_kwargs = {
    "timeout": 60,
    "proxies": None,
    "stream": False,
    "verify": True,
    "cert": None,
}
HOST_ADDRESS = "http://example.com"
URL = "/api/resource"
DATA_VALUE = "value"
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
    return mocker.MagicMock(spec=C42RenewableAuth)


@pytest.fixture
def mock_key_value_service(mocker):
    return mocker.MagicMock(spec=KeyValueStoreClient)


@pytest.fixture
def mock_server_env_conn(mocker):
    mock_conn = mocker.MagicMock(spec=Connection)
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = '{"stsBaseUrl": "sts-testsuffix"}'
    mock_conn.get.return_value = Py42Response(mock_response)
    return mock_conn


@pytest.fixture
def mock_server_env_conn_missing_sts_base_url(mocker):
    mock_conn = mocker.MagicMock(spec=Connection)
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.text = "{}"
    mock_conn.get.return_value = Py42Response(mock_response)
    return mock_conn


class MockPreparedRequest(object):
    def __init__(self, method, url, data=None):
        self._method = method
        self._url = url
        self._data = data

    def __eq__(self, other):
        return (
            self._method == other.method
            and self._url == other.url
            and self._data == other.body
        )


class TestKnownUrlHostResolver(object):
    def test_get_host_address_returns_expected_value(self):
        resolver = KnownUrlHostResolver(HOST_ADDRESS)
        assert resolver.get_host_address() == HOST_ADDRESS


class TestMicroserviceKeyHostResolver(object):
    def test_get_host_address_returns_expected_value(self, mock_key_value_service):
        mock_key_value_service.get_stored_value.return_value.text = HOST_ADDRESS
        resolver = MicroserviceKeyHostResolver(mock_key_value_service, "TEST_KEY")
        assert resolver.get_host_address() == HOST_ADDRESS

    def test_get_host_address_passes_expected_key(self, mock_key_value_service):
        resolver = MicroserviceKeyHostResolver(mock_key_value_service, "TEST_KEY")
        resolver.get_host_address()
        mock_key_value_service.get_stored_value.assert_called_once_with("TEST_KEY")


class TestMicroservicePrefixHostResolver(object):
    def test_get_host_address_returns_expected_value(self, mock_server_env_conn):
        resolver = MicroservicePrefixHostResolver(mock_server_env_conn, "TESTPREFIX")
        assert resolver.get_host_address() == "TESTPREFIX-testsuffix"

    def test_get_host_address_when_sts_base_url_not_found_raises_feature_unavailable_error(
        self, mock_server_env_conn_missing_sts_base_url
    ):
        resolver = MicroservicePrefixHostResolver(
            mock_server_env_conn_missing_sts_base_url, "TESTPREFIX"
        )
        with pytest.raises(Py42FeatureUnavailableError):
            resolver.get_host_address()

    def test_get_host_address_calls_correct_server_env_url(self, mock_server_env_conn):
        resolver = MicroservicePrefixHostResolver(mock_server_env_conn, "TESTPREFIX")
        resolver.get_host_address()
        mock_server_env_conn.get.assert_called_once_with("/api/ServerEnv")


class TestConnection(object):
    def test_connection_get_calls_requests_with_get(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.get(URL)
        expected = MockPreparedRequest("GET", HOST_ADDRESS + URL, None)
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_put_calls_requests_with_put(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.put(URL, data="testdata")
        expected = MockPreparedRequest("PUT", HOST_ADDRESS + URL, "testdata")
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_post_calls_requests_with_post(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.post(URL, data="testdata")
        expected = MockPreparedRequest("POST", HOST_ADDRESS + URL, "testdata")
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_patch_calls_requests_with_patch(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.patch(URL, data="testdata")
        expected = MockPreparedRequest("PATCH", HOST_ADDRESS + URL, "testdata")
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_delete_calls_requests_with_delete(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.delete(URL)
        expected = MockPreparedRequest("DELETE", HOST_ADDRESS + URL)
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_options_calls_requests_with_options(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.options(URL)
        expected = MockPreparedRequest("OPTIONS", HOST_ADDRESS + URL)
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_head_calls_requests_with_head(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.head(URL)
        expected = MockPreparedRequest("HEAD", HOST_ADDRESS + URL)
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_post_with_json_prepares_request_with_string_encoded_json_body(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.post(URL, json=JSON_VALUE)
        expected = MockPreparedRequest(
            "POST", HOST_ADDRESS + URL, json.dumps(JSON_VALUE)
        )
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

    def test_connection_post_with_data_and_json_params_overwrites_data_with_json(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.post(URL, data=DATA_VALUE, json=JSON_VALUE)
        expected = MockPreparedRequest(
            "POST", HOST_ADDRESS + URL, json.dumps(JSON_VALUE)
        )
        success_requests_session.send.assert_called_once_with(
            expected, **default_kwargs
        )

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
        with pytest.raises(Py42InternalServerError):
            connection.get(URL)

    def test_connection_request_calls_auth_handler_when_making_first_request(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        connection.get(URL)
        assert mock_auth.call_count == 1

    def test_connection_request_calls_auth_handler_clears_renews_credentials_when_response_unauthorized(
        self, mock_host_resolver, mock_auth, renewed_requests_session
    ):
        connection = Connection(mock_host_resolver, mock_auth, renewed_requests_session)
        connection.get(URL)
        assert renewed_requests_session.send.call_count == 2
        assert mock_auth.call_count == 2
        assert mock_auth.clear_credentials.call_count == 1

    def test_connection_request_raises_unauthorized_error_when_renewal_results_in_401(
        self, mock_host_resolver, mock_auth, unauthorized_requests_session
    ):
        connection = Connection(
            mock_host_resolver, mock_auth, unauthorized_requests_session
        )

        with pytest.raises(Py42UnauthorizedError):
            connection.get(URL)

        assert unauthorized_requests_session.send.call_count == 2

    def test_connection_request_when_session_returns_none_raises_py42_error(
        self, mock_host_resolver, mock_auth, success_requests_session
    ):
        success_requests_session.send.return_value = None
        connection = Connection(mock_host_resolver, mock_auth, success_requests_session)
        with pytest.raises(Py42Error):
            connection.get(URL)
