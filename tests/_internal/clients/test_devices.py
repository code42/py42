# -*- coding: utf-8 -*-

import pytest

from py42._internal.session import Py42Session
from py42._internal.clients.devices import DeviceClient


COMPUTER_URI = "/api/Computer"

DEFAULT_GET_DEVICES_PARAMS = {
    "active": None,
    "blocked": None,
    "orgUid": None,
    "userUid": None,
    "targetComputerGuid": None,
    "incBackupUsage": None,
    "incCounts": True,
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

    def test_get_devices_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = DeviceClient(session, v3_required_session)
        client.get_devices(q="TEST-HOSTNAME")
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = "TEST-HOSTNAME"
        session.get.assert_called_with(COMPUTER_URI, params=DEFAULT_GET_DEVICES_PARAMS)

    def test_unicode_hostname_get_devices_calls_get_with_unicode_q_param(self, session, v3_required_session):
        unicode_hostname = u"我能吞"
        client = DeviceClient(session, v3_required_session)
        client.get_devices(q=unicode_hostname)
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = unicode_hostname
        session.get.assert_called_with(COMPUTER_URI, params=expected_params)
