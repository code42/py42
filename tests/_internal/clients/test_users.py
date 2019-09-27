# -*- coding: utf-8 -*-

import pytest
from requests import Response

from py42._internal.clients.users import UserClient
from py42._internal.session import Py42Session

USER_URI = "/api/User"

DEFAULT_GET_USERS_PARAMS = {
    "active": None,
    "userUid": None,
    "email": None,
    "orgUid": None,
    "roleId": None,
    "pgNum": None,
    "pgSize": None,
    "q": None,
}

MOCK_GET_USER_RESPONSE = """{
  "data": {"totalCount": 3000, "users":[]} 
}"""


class TestUserClient(object):
    def _mock_callback(self, response):
        pass

    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def v3_required_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def mock_get_users(self, mocker):
        def get_users(then=None, *args, **kwargs):
            response = mocker.MagicMock(spec=Response)
            response.status_code = 200
            response.text = MOCK_GET_USER_RESPONSE
            return then(response)

        return get_users

    def test_get_users_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = UserClient(session, v3_required_session)
        client.get_users()
        session.get.assert_called_once_with(USER_URI, params=DEFAULT_GET_USERS_PARAMS)

    def test_unicode_username_get_user_by_username_calls_get_with_username(
        self, session, v3_required_session
    ):
        username = u"您已经发现了秘密信息"
        client = UserClient(session, v3_required_session)
        client.get_user_by_username(username)
        expected_params = {u"username": username}
        session.get.assert_called_once_with(USER_URI, params=expected_params)

    def test_for_each_user_calls_get_users_once_per_page(
        self, session, v3_required_session, mocker, mock_get_users
    ):
        client = UserClient(session, v3_required_session)
        client.get_users = mocker.MagicMock()
        client.get_users.side_effect = mock_get_users

        client.for_each_user(then=self._mock_callback)
        assert client.get_users.call_count == 3

    def test_for_each_user_calls_get_users_with_correct_args_each_time(
        self, session, v3_required_session, mocker, mock_get_users
    ):
        client = UserClient(session, v3_required_session)
        client.get_users = mocker.MagicMock()
        client.get_users.side_effect = mock_get_users

        calls = []
        for i in range(3):
            calls.append(
                mocker.call(
                    active="active",
                    email="email",
                    org_uid="org_uid",
                    role_id="role_id",
                    page_num=i + 1,
                    page_size=mocker.ANY,
                    then=mocker.ANY,
                )
            )
        client.for_each_user(
            active="active",
            email="email",
            org_uid="org_uid",
            role_id="role_id",
            then=self._mock_callback,
        )
        client.get_users.assert_has_calls(calls)

    def test_get_user_by_id_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = UserClient(session, v3_required_session)
        client.get_user_by_id("USER_ID")
        uri = "{0}/{1}".format(USER_URI, "USER_ID")
        session.get.assert_called_once_with(uri)
