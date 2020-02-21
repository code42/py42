# -*- coding: utf-8 -*-

import pytest
from requests import Response

import py42
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
    "pgNum": 1,
    "pgSize": 1000,
    "q": None,
}

MOCK_GET_DEVICE_RESPONSE = """{
  "data": {"totalCount": 3000, "computers":["foo"]} 
}"""

MOCK_EMPTY_GET_DEVICE_RESPONSE = """{
  "data": {"totalCount": 3000, "computers":[]} 
}"""


class TestDeviceClient(object):
    @pytest.fixture
    def mock_get_devices_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_GET_DEVICE_RESPONSE
        return response

    @pytest.fixture
    def mock_get_devices_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_EMPTY_GET_DEVICE_RESPONSE
        return response

    def test_get_devices_calls_get_with_uri_and_params(
        self, session, v3_required_session, mock_get_devices_response
    ):
        client = DeviceClient(session, v3_required_session)
        session.get.return_value = mock_get_devices_response
        for page in client.get_devices(q="TEST-HOSTNAME"):
            break
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = "TEST-HOSTNAME"
        first_call = session.get.call_args_list[0]
        assert first_call[0][0] == COMPUTER_URI
        assert first_call[1]["params"] == DEFAULT_GET_DEVICES_PARAMS

    def test_unicode_hostname_get_devices_calls_get_with_unicode_q_param(
        self, session, v3_required_session, mock_get_devices_response
    ):
        unicode_hostname = u"您已经发现了秘密信息"
        client = DeviceClient(session, v3_required_session)
        session.get.return_value = mock_get_devices_response
        for page in client.get_devices(q=unicode_hostname):
            break
        first_call = session.get.call_args_list[0]
        assert first_call[0][0] == COMPUTER_URI
        params = DEFAULT_GET_DEVICES_PARAMS
        params["q"] = unicode_hostname
        assert first_call[1]["params"] == params

    def test_get_device_by_id_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = DeviceClient(session, v3_required_session)
        client.get_device_by_id("DEVICE_ID", include_backup_usage=True)
        expected_params = {"incBackupUsage": True}
        uri = "{0}/{1}".format(COMPUTER_URI, "DEVICE_ID")
        session.get.assert_called_once_with(uri, params=expected_params)

    def test_get_devices_calls_get_expected_number_of_times(
        self,
        session,
        v3_required_session,
        mock_get_devices_response,
        mock_get_devices_empty_response,
    ):
        py42.settings.items_per_page = 1
        client = DeviceClient(session, v3_required_session)
        session.get.side_effect = [
            mock_get_devices_response,
            mock_get_devices_response,
            mock_get_devices_empty_response,
        ]
        for page in client.get_devices():
            pass
        py42.settings.items_per_page = 1000
        assert session.get.call_count == 3
