# -*- coding: utf-8 -*-

import pytest

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
    "q": None
}


class TestDeviceClient(object):

    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def v3_required_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    def test_get_users_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = UserClient(session, v3_required_session)
        client.get_users()
        session.get.assert_called_with(USER_URI, params=DEFAULT_GET_USERS_PARAMS)

    def test_unicode_username_get_user_by_username_calls_get_with_username(self, session, v3_required_session):
        username = u"我能吞"
        client = UserClient(session, v3_required_session)
        client.get_user_by_username(username)
        expected_params = {"username": username}
        session.get.assert_called_with(USER_URI, params=expected_params)
