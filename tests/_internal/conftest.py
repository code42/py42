import pytest
from requests import Session, Response

from requests import HTTPError

from py42._internal.auth_handling import AuthHandler

import py42.settings

HOST_ADDRESS = "http://example.com"

URL = "/api/resource"
DATA_VALUE = "value"
JSON_VALUE = {"key": "value"}

KWARGS_INDEX = 1
DATA_KEY = "data"
JSON_KEY = "json"

TEST_RESPONSE_CONTENT = "test_response_content"

REQUEST_EXCEPTION_MESSAGE = "Internal server error"
TRACEBACK = "Traceback..."


def build_expected_exception_message(host, url, exception_type, exception_message):
    message_format = "Error making request to {0}{1}. Caused by: {2}('{3}',)"
    return message_format.format(host, url, exception_type.__name__, exception_message)


def build_expected_exception_message_with_trace(host, url, exception_type, exception_message, trace):
    return build_expected_exception_message(host, url, exception_type, exception_message) + " " + repr(trace)


@pytest.fixture
def successful_response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.content = TEST_RESPONSE_CONTENT
    response.status_code = 200
    return response


@pytest.fixture
def error_response(mocker, http_error):
    response = mocker.MagicMock(spec=Response)
    response.content = ""
    response.status_code = 500
    response.raise_for_status.side_effect = http_error
    return response


@pytest.fixture
def http_error():
    return HTTPError(REQUEST_EXCEPTION_MESSAGE)


@pytest.fixture
def traceback(mocker):
    format_exc = mocker.patch("traceback.format_exc")
    format_exc.return_value = TRACEBACK
    return format_exc


@pytest.fixture
def success_requests_session(mocker, successful_response):
    session = mocker.MagicMock(spec=Session)
    session.request.return_value = successful_response
    return session


@pytest.fixture
def error_requests_session(mocker, error_response):
    session = mocker.MagicMock(spec=Session)
    session.request.return_value = error_response
    return session


@pytest.fixture
def valid_auth_handler(mocker):
    auth_handler = mocker.MagicMock(spec=AuthHandler)
    auth_handler.response_indicates_unauthorized.return_value = False
    return auth_handler


@pytest.fixture
def renewing_auth_handler(mocker):
    auth_handler = mocker.MagicMock(spec=AuthHandler)
    # initialized, unauthorized, corrected
    auth_handler.response_indicates_unauthorized.side_effect = [False, True, False]
    return auth_handler


@pytest.fixture
def catch(mocker):
    return mocker.MagicMock()


@pytest.fixture
def global_exception_message_receiver(mocker):
    receiver = mocker.MagicMock()
    py42.settings.global_exception_message_receiver = receiver
    return receiver


@pytest.fixture
def exception():
    return Exception()