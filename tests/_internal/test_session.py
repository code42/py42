from json import dumps

import pytest
from requests import Session, Response

from py42._internal.auth_handling import AuthHandler
from py42._internal.session import Py42Session

HOST_ADDRESS = "http://example.com"

URL = "/api/resource"
DATA_VALUE = "value"
JSON_VALUE = {"key": "value"}

KWARGS_INDEX = 1
DATA_KEY = "data"
JSON_KEY = "json"

TEST_RESPONSE_CONTENT = "test_response_content"


@pytest.fixture
def successful_response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.content = TEST_RESPONSE_CONTENT
    response.status_code = 200
    return response


@pytest.fixture
def error_response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.content = ""
    response.status_code = 500
    response.did_raise = False

    def raise_for_status():
        response.did_raise = True

    response.raise_for_status = raise_for_status
    return response


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


def test_session_post_with_json_calls_filter_out_none_util(mocker, success_requests_session):
    session = Py42Session(success_requests_session, HOST_ADDRESS)
    filter_out_none_mock = mocker.patch("py42.util.filter_out_none")
    filter_out_none_mock.return_value = {}

    session.post(URL, json=JSON_VALUE)

    filter_out_none_mock.assert_called()


def test_session_post_with_json_calls_request_with_data_param_with_string_encoded_json(success_requests_session):
    session = Py42Session(success_requests_session, HOST_ADDRESS)
    session.post(URL, json=JSON_VALUE)
    assert success_requests_session.request.call_args[KWARGS_INDEX][DATA_KEY] == dumps(JSON_VALUE)


def test_session_post_with_data_and_json_params_overwrites_data_with_json(success_requests_session):
    session = Py42Session(success_requests_session, HOST_ADDRESS)
    session.post(URL, data=DATA_VALUE, json=JSON_VALUE)
    assert success_requests_session.request.call_args[KWARGS_INDEX][DATA_KEY] == dumps(JSON_VALUE)


def test_session_post_with_data_and_json_params_does_not_pass_json_param_to_request(success_requests_session):
    session = Py42Session(success_requests_session, HOST_ADDRESS)
    session.post(URL, data=DATA_VALUE, json=JSON_VALUE)
    assert success_requests_session.request.call_args[KWARGS_INDEX].get(JSON_KEY) is None


def test_session_request_returns_response_when_good_status_code(success_requests_session):
    session = Py42Session(success_requests_session, HOST_ADDRESS)
    response = session.get(URL)
    assert response.content == TEST_RESPONSE_CONTENT


def test_session_request_calls_raise_for_status_on_response_with_error_status_code(error_requests_session):
    session = Py42Session(error_requests_session, HOST_ADDRESS)
    response = session.get(URL)
    assert response.did_raise


def test_session_request_calls_auth_handler_renew_authentication_with_correct_params_when_making_first_request(success_requests_session, valid_auth_handler):
    session = Py42Session(success_requests_session, HOST_ADDRESS, valid_auth_handler)
    session.get(URL)
    valid_auth_handler.renew_authentication.assert_called_with(session, use_credential_cache=True)


def test_session_request_calls_auth_handler_renew_authentication_only_once_while_auth_is_valid(success_requests_session, valid_auth_handler):
    session = Py42Session(success_requests_session, HOST_ADDRESS, valid_auth_handler)
    session.get(URL)
    session.get(URL)
    valid_auth_handler.renew_authentication.assert_called_once()


def test_session_request_calls_auth_handler_renew_authentication_twice_when_response_unauthorized(success_requests_session, renewing_auth_handler):
    session = Py42Session(success_requests_session, HOST_ADDRESS, renewing_auth_handler)
    session.get(URL)  # initialize
    assert success_requests_session.request.call_count == 1
    session.get(URL)  # second request will be unauthorized and call renew_authentication again
    assert renewing_auth_handler.renew_authentication.call_count == 2


def test_session_request_called_again_twice_when_response_unauthorized(success_requests_session, renewing_auth_handler):
    session = Py42Session(success_requests_session, HOST_ADDRESS, renewing_auth_handler)
    session.get(URL)  # initialize
    assert success_requests_session.request.call_count == 1
    session.get(URL)  # second request will be unauthorized and call request again
    assert success_requests_session.request.call_count == 3
