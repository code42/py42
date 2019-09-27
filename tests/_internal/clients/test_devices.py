# -*- coding: utf-8 -*-

import pytest
from requests import Response

from py42._internal.clients.devices import DeviceClient
from py42._internal.session import Py42Session

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
    "q": None,
}

MOCK_GET_DEVICE_RESPONSE = """{
  "data": {"totalCount": 3000, "computers":[]} 
}"""


class TestDeviceClient(object):
    def _mock_callback(self, response):
        pass

    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def v3_required_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def mock_get_devices(self, mocker):
        def get_devices(then=None, *args, **kwargs):
            response = mocker.MagicMock(spec=Response)
            response.status_code = 200
            response.text = MOCK_GET_DEVICE_RESPONSE
            return then(response)

        return get_devices

    def test_get_devices_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = DeviceClient(session, v3_required_session)
        client.get_devices(q="TEST-HOSTNAME")
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = "TEST-HOSTNAME"
        session.get.assert_called_once_with(COMPUTER_URI, params=DEFAULT_GET_DEVICES_PARAMS)

    def test_unicode_hostname_get_devices_calls_get_with_unicode_q_param(
        self, session, v3_required_session
    ):
        unicode_hostname = u"您已经发现了秘密信息"
        client = DeviceClient(session, v3_required_session)
        client.get_devices(q=unicode_hostname)
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = unicode_hostname
        session.get.assert_called_once_with(COMPUTER_URI, params=expected_params)

    def test_for_each_device_calls_get_devices_once_per_page(
        self, session, v3_required_session, mocker, mock_get_devices
    ):
        client = DeviceClient(session, v3_required_session)
        client.get_devices = mocker.MagicMock()
        client.get_devices.side_effect = mock_get_devices

        client.for_each_device(then=self._mock_callback)
        assert client.get_devices.call_count == 3

    def test_for_each_device_calls_get_devices_with_same_args_each_time(
        self, session, v3_required_session, mocker, mock_get_devices
    ):
        client = DeviceClient(session, v3_required_session)
        client.get_devices = mocker.MagicMock()
        client.get_devices.side_effect = mock_get_devices

        calls = []
        for i in range(3):
            mocker.call(
                active="active",
                org_uid="org_uid",
                user_uid="user_uid",
                target_computer_guid="target_computer_guid",
                include_backup_usage=False,
                include_counts=True,
                page_num=i + 1,
                page_size=mocker.ANY,
                then=mocker.ANY,
            )
        client.for_each_device(
            active="active",
            org_uid="org_uid",
            user_uid="user_uid",
            target_computer_guid="target_computer_guid",
            include_backup_usage=False,
            then=self._mock_callback,
        )
        client.get_devices.assert_has_calls(calls)

    def test_get_device_by_id_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = DeviceClient(session, v3_required_session)
        client.get_device_by_id("DEVICE_ID", include_backup_usage=True)
        expected_params = {"incBackupUsage": True}
        uri = "{0}/{1}".format(COMPUTER_URI, "DEVICE_ID")
        session.get.assert_called_once_with(uri, params=expected_params)
