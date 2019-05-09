from json import dumps

import pytest
from requests import Session

from py42._internal.session import Py42Session

HOST_ADDRESS = "http://example.com"

URL = "/api/resource"
DATA_VALUE = "value"
JSON_VALUE = {"key": "value"}

KWARGS_INDEX = 1
DATA_KEY = "data"
JSON_KEY = "json"


@pytest.fixture
def base_session(mocker):
    return mocker.MagicMock(spec=Session)


def test_session_post_with_json_calls_filter_out_none_util(mocker, base_session):
    session = Py42Session(base_session, HOST_ADDRESS)
    filter_out_none_mock = mocker.patch("py42.util.filter_out_none")
    filter_out_none_mock.return_value = {}

    session.post(URL, json=JSON_VALUE)

    filter_out_none_mock.assert_called()


def test_session_post_with_json_calls_request_with_data_param_with_string_encoded_json(base_session):
    session = Py42Session(base_session, HOST_ADDRESS)
    session.post(URL, json=JSON_VALUE)
    assert base_session.request.call_args[KWARGS_INDEX][DATA_KEY] == dumps(JSON_VALUE)


def test_session_post_with_data_and_json_params_overwrites_data_with_json(base_session):
    session = Py42Session(base_session, HOST_ADDRESS)
    session.post(URL, data=DATA_VALUE, json=JSON_VALUE)
    assert base_session.request.call_args[KWARGS_INDEX][DATA_KEY] == dumps(JSON_VALUE)


def test_session_post_with_data_and_json_params_does_not_pass_json_param_to_request(base_session):
    session = Py42Session(base_session, HOST_ADDRESS)
    session.post(URL, data=DATA_VALUE, json=JSON_VALUE)
    assert base_session.request.call_args[KWARGS_INDEX].get(JSON_KEY) is None
