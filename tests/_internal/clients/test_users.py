# -*- coding: utf-8 -*-

import pytest
from requests import Response

from py42._internal.clients.users import UserClient
from py42._internal.session import Py42Session
import py42.settings as settings

USER_URI = "/api/User"

DEFAULT_GET_USERS_PARAMS = {
    "active": None,
    "email": None,
    "orgUid": None,
    "roleId": None,
    "pgNum": 1,
    "pgSize": 1,
    "q": None,
}

MOCK_GET_USER_RESPONSE = """{
  "data": {"totalCount": 3000, "users":["foo"]} 
}"""

MOCK_EMPTY_GET_USER_RESPONSE = """{
  "data": {"totalCount": 3000, "users":[]} 
}"""

settings.items_per_page = 1


class TestUserClient(object):
    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def v3_required_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def mock_get_users(self, mocker):
        def get_devices(*args, **kwargs):
            response = mocker.MagicMock(spec=Response)
            response.status_code = 200
            response.text = MOCK_GET_USER_RESPONSE
            return response

        return get_devices

    @pytest.fixture
    def mock_get_users_empty(self, mocker):
        def get_devices(*args, **kwargs):
            response = mocker.MagicMock(spec=Response)
            response.status_code = 200
            response.text = MOCK_EMPTY_GET_USER_RESPONSE
            return response

        return get_devices

    def test_get_users_calls_get_with_uri_and_params(
        self, session, v3_required_session, mock_get_users, mock_get_users_empty
    ):
        session.get.side_effect = [mock_get_users(), mock_get_users_empty()]
        client = UserClient(session, v3_required_session)
        for page in client.get_users():
            pass
        first_call = session.get.call_args_list[0]
        assert first_call[0][0] == USER_URI
        assert first_call[1]["params"] == DEFAULT_GET_USERS_PARAMS

    def test_unicode_username_get_user_by_username_calls_get_with_username(
        self, session, v3_required_session
    ):
        username = u"您已经发现了秘密信息"
        client = UserClient(session, v3_required_session)
        client.get_user_by_username(username)
        expected_params = {u"username": username}
        session.get.assert_called_once_with(USER_URI, params=expected_params)

    def test_get_user_by_id_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = UserClient(session, v3_required_session)
        client.get_user_by_id("USER_ID")
        uri = "{0}/{1}".format(USER_URI, "USER_ID")
        session.get.assert_called_once_with(uri)

    def test_get_users_calls_get_expected_number_of_times(
        self, session, v3_required_session, mock_get_users, mock_get_users_empty
    ):
        client = UserClient(session, v3_required_session)
        session.get.side_effect = [mock_get_users(), mock_get_users(), mock_get_users_empty()]
        for page in client.get_users():
            pass
        assert session.get.call_count == 3
