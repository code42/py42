# -*- coding: utf-8 -*-

import pytest
from requests import HTTPError, Response, Session
from requests.cookies import RequestsCookieJar

from py42._internal.auth_handling import AuthHandler
from py42._internal.filters.query_filter import QueryFilter


from py42._internal.session import Py42Session

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


EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"您已经发现了秘密信息"

cookie_dict = {}


@pytest.fixture
def successful_response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.text = TEST_RESPONSE_CONTENT
    response.status_code = 200
    response.encoding = None
    return response


@pytest.fixture
def error_response(mocker, http_error):
    response = mocker.MagicMock(spec=Response)
    response.text = ""
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
def exception():
    return Exception()


@pytest.fixture
def query_filter_list(query_filter):
    return [query_filter for _ in range(3)]


@pytest.fixture
def query_filter():
    return QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


@pytest.fixture
def unicode_query_filter():
    return QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_UNICODE)


@pytest.fixture
def mock_session(mocker):
    session = mocker.MagicMock(spec=Py42Session)
    session.headers = {}
    session.cookies = mocker.MagicMock(spec=RequestsCookieJar)

    def get_cookie(name):
        return cookie_dict.get(name, None)

    def set_cookie(name, value):
        cookie_dict.update({name: value})

    session.cookies.get = get_cookie
    session.cookies.set = set_cookie

    return session
