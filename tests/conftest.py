# -*- coding: utf-8 -*-
import json

import pytest
from requests import HTTPError
from requests import Response
from requests import Session

from py42.exceptions import Py42UnauthorizedError
from py42.response import Py42Response
from py42.sdk.queries.query_filter import QueryFilter
from py42.services._connection import Connection
from py42.usercontext import UserContext

TENANT_ID_FROM_RESPONSE = "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def user_context(mocker):
    client = mocker.MagicMock(spec=UserContext)
    client.get_current_tenant_id.return_value = TENANT_ID_FROM_RESPONSE
    return client


HOST_ADDRESS = "http://example.com"

URL = "/api/resource"
DATA_VALUE = "value"
JSON_VALUE = {"key": "value"}

KWARGS_INDEX = 1
DATA_KEY = "data"
JSON_KEY = "json"

TEST_RESPONSE_CONTENT = '{"key":"test_response_content"}'

REQUEST_EXCEPTION_MESSAGE = "Internal server error"
TRACEBACK = "Traceback..."


EVENT_FILTER_FIELD_NAME = "filter_field_name"
OPERATOR_STRING = "IS_IN"
VALUE_STRING = "value_example"
VALUE_UNICODE = u"您已经发现了秘密信息"


@pytest.fixture
def http_error():
    return HTTPError(REQUEST_EXCEPTION_MESSAGE)


@pytest.fixture
def successful_response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.text = TEST_RESPONSE_CONTENT
    response.status_code = 200
    response.encoding = None
    return response


@pytest.fixture
def error_response(mocker, http_error):
    error = http_error
    error.response = mocker.MagicMock(spec=Response)
    error.response.text = ""
    error.response.status_code = 500
    error.response.raise_for_status.side_effect = http_error
    return error


@pytest.fixture
def unauthorized_response(mocker, http_error):
    response = mocker.MagicMock(spec=Response)
    response.text = TEST_RESPONSE_CONTENT
    response.status_code = 401
    response.encoding = None
    response.raise_for_status.side_effect = [Py42UnauthorizedError(http_error)]
    return response


@pytest.fixture
def py42_response(mocker):
    response = mocker.MagicMock(spec=Py42Response)
    response.status_code = 200
    response.encoding = None
    response.__getitem__ = lambda _, key: json.loads(response.text)[key]
    return response


@pytest.fixture
def traceback(mocker):
    format_exc = mocker.patch("traceback.format_exc")
    format_exc.return_value = TRACEBACK
    return format_exc


@pytest.fixture
def success_requests_session(mocker, successful_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    session.send.return_value = successful_response
    return session


@pytest.fixture
def error_requests_session(mocker, error_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    session.send.return_value = error_response.response
    return session


@pytest.fixture
def unauthorized_requests_session(mocker, unauthorized_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    session.send.return_value = unauthorized_response
    return session


@pytest.fixture
def renewed_requests_session(mocker, unauthorized_response, successful_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    # unauthorized, then corrected
    session.send.side_effect = [unauthorized_response, successful_response]
    return session


@pytest.fixture
def exception():
    return Exception()


@pytest.fixture
def query_filter_list():
    return [
        QueryFilter(
            EVENT_FILTER_FIELD_NAME + str(suffix),
            OPERATOR_STRING + str(suffix),
            VALUE_STRING + str(suffix),
        )
        for suffix in range(3)
    ]


@pytest.fixture
def query_filter():
    return QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_STRING)


@pytest.fixture
def unicode_query_filter():
    return QueryFilter(EVENT_FILTER_FIELD_NAME, OPERATOR_STRING, VALUE_UNICODE)


@pytest.fixture
def mock_connection(mocker):
    connection = mocker.MagicMock(spec=Connection)
    connection.headers = {}

    return connection


@pytest.fixture
def mock_successful_connection(mock_connection, successful_response):
    mock_connection.get.return_value = successful_response
    return mock_connection
