# -*- coding: utf-8 -*-

import pytest

from requests import Response
import json

import py42
from py42._internal.clients.users import UserClient
from py42._internal.session import Py42Session


USER_URI = "/api/User"

DEFAULT_GET_ALL_PARAMS = {
    "active": None,
    "email": None,
    "orgUid": None,
    "roleId": None,
    "pgNum": 1,
    "pgSize": 1000,
    "q": None,
}

MOCK_GET_USER_RESPONSE = """{
  "data": {"totalCount": 3000, "users":["foo"]}
}"""

MOCK_EMPTY_GET_USER_RESPONSE = """{
  "data": {"totalCount": 3000, "users":[]}
}"""

MOCK_API_RESPONSE_TEXT = '{"data": {"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}}'


class TestUserClient(object):
    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def mock_get_all_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_GET_USER_RESPONSE
        return response

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_EMPTY_GET_USER_RESPONSE
        return response

    @pytest.fixture
    def post_api_mock_response(self, mocker):
        api_mock_response = mocker.MagicMock(spec=Response)
        api_mock_response.text = MOCK_API_RESPONSE_TEXT
        return api_mock_response

    def test_post_create_user_is_successful(self, session, post_api_mock_response):
        user_client = UserClient(session)
        session.post.return_value = post_api_mock_response
        org_uid = "TEST_ORG_ID"
        username = "TEST_ORG@TEST.COM"
        password = "password"
        name = "TESTNAME"
        note = "Test Note"
        user_client.create_user(org_uid, username, username, password, name, name, note)
        expected_params = {
            u"orgUid": org_uid,
            u"username": username,
            u"email": username,
            u"password": password,
            u"firstName": name,
            u"lastName": name,
            u"notes": note,
        }

        session.post.assert_called_once_with(USER_URI, data=json.dumps(expected_params))

    def test_get_users_calls_get_with_uri_and_params(self, session, mock_get_all_response):
        session.get.side_effect = mock_get_all_response
        client = UserClient(session)
        for _ in client.get_all():
            break
        first_call = session.get.call_args_list[0]
        assert first_call[0][0] == USER_URI
        assert first_call[1]["params"] == DEFAULT_GET_ALL_PARAMS

    def test_unicode_username_get_user_by_username_calls_get_with_username(self, session):
        username = u"您已经发现了秘密信息"
        client = UserClient(session)
        client.get_by_username(username)
        expected_params = {u"username": username}
        session.get.assert_called_once_with(USER_URI, params=expected_params)

    def test_get_user_by_id_calls_get_with_uri_and_params(self, session):
        client = UserClient(session)
        client.get_by_id("USER_ID")
        uri = "{0}/{1}".format(USER_URI, "USER_ID")
        session.get.assert_called_once_with(uri, params={})

    def test_get_users_calls_get_expected_number_of_times(
        self, session, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.settings.items_per_page = 1
        client = UserClient(session)
        session.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in client.get_all():
            pass
        py42.settings.items_per_page = 1000
        assert session.get.call_count == 3
