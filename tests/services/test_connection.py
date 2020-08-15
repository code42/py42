import json

import pytest

from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42UnauthorizedError
from py42.services._auth import C42RenewableAuth
from py42.services._connection import Connection
from py42.services._connection import HostResolver

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
