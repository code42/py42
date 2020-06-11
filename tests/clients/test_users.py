# -*- coding: utf-8 -*-

import json

import pytest
from requests import Response

import py42
import py42.settings
from py42.clients.users import UserClient
from py42.response import Py42Response

USER_URI = "/api/User"

DEFAULT_GET_ALL_PARAMS = {
    "active": None,
    "email": None,
    "orgUid": None,
    "roleId": None,
    "pgNum": 1,
    "pgSize": 500,
    "q": None,
}

MOCK_GET_USER_RESPONSE = """{"totalCount": 3000, "users": ["foo"]}"""

MOCK_EMPTY_GET_USER_RESPONSE = """{"totalCount": 3000, "users": []}"""

MOCK_text = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'


class TestUserClient(object):
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_USER_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_USER_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def post_api_mock_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_text
        return Py42Response(response)

    def test_post_create_user_is_successful(self, mock_session, post_api_mock_response):
        user_client = UserClient(mock_session)
        mock_session.post.return_value = post_api_mock_response
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

        mock_session.post.assert_called_once_with(USER_URI, data=json.dumps(expected_params))

    def test_get_all_calls_get_with_uri_and_params(self, mock_session, mock_get_all_response):
        mock_session.get.side_effect = [mock_get_all_response]
        client = UserClient(mock_session)
        for _ in client.get_all():
            break
        first_call = mock_session.get.call_args_list[0]
        assert first_call[0][0] == USER_URI
        assert first_call[1]["params"] == DEFAULT_GET_ALL_PARAMS

    def test_unicode_username_get_user_by_username_calls_get_with_username(
        self, mock_session, successful_response
    ):
        username = u"您已经发现了秘密信息"
        mock_session.get.return_value = successful_response
        client = UserClient(mock_session)
        client.get_by_username(username)
        expected_params = {u"username": username}
        mock_session.get.assert_called_once_with(USER_URI, params=expected_params)

    def test_get_user_by_id_calls_get_with_uri_and_params(self, mock_session, successful_response):
        mock_session.get.return_value = successful_response
        client = UserClient(mock_session)
        client.get_by_id("USER_ID")
        uri = "{0}/{1}".format(USER_URI, "USER_ID")
        mock_session.get.assert_called_once_with(uri, params={})

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_session, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.settings.items_per_page = 1
        client = UserClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in client.get_all():
            pass
        py42.settings.items_per_page = 500
        assert mock_session.get.call_count == 3

    def test_get_scim_data_by_uid_calls_get_with_expected_uri_and_params(self, mock_session):
        client = UserClient(mock_session)
        client.get_scim_data_by_uid("USER_ID")
        uri = "/api/v7/scim-user-data/collated-view"
        mock_session.get.assert_called_once_with(uri, params={"userId": "USER_ID"})
