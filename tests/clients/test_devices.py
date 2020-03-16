# -*- coding: utf-8 -*-
import json

import pytest
from requests import Response

import py42
from py42.clients.devices import DeviceClient
from py42.sdk.response import Py42Response

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

MOCK_GET_DEVICE_RESPONSE = """{"totalCount": 3000, "computers":["foo"]}"""

MOCK_EMPTY_GET_DEVICE_RESPONSE = """{"totalCount": 3000, "computers":[]}"""


class TestDeviceClient(object):
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_DEVICE_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker, py42_response):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_DEVICE_RESPONSE
        return Py42Response(response)

    def test_get_devices_calls_get_with_uri_and_params(self, mock_session, mock_get_all_response):
        client = DeviceClient(mock_session)
        mock_session.get.return_value = mock_get_all_response
        for _ in client.get_all(q="TEST-HOSTNAME"):
            break
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = "TEST-HOSTNAME"
        first_call = mock_session.get.call_args_list[0]
        assert first_call[0][0] == COMPUTER_URI
        assert first_call[1]["params"] == DEFAULT_GET_DEVICES_PARAMS

    def test_unicode_hostname_get_devices_calls_get_with_unicode_q_param(
        self, mock_session, mock_get_all_response
    ):
        unicode_hostname = u"您已经发现了秘密信息"
        client = DeviceClient(mock_session)
        mock_session.get.return_value = mock_get_all_response
        for _ in client.get_all(q=unicode_hostname):
            break
        first_call = mock_session.get.call_args_list[0]
        assert first_call[0][0] == COMPUTER_URI
        params = DEFAULT_GET_DEVICES_PARAMS
        params["q"] = unicode_hostname
        assert first_call[1]["params"] == params

    def test_get_by_id_calls_get_with_uri_and_params(self, mock_session, successful_response):
        mock_session.get.return_value = successful_response
        client = DeviceClient(mock_session)
        client.get_by_id("DEVICE_ID", include_backup_usage=True)
        expected_params = {"incBackupUsage": True}
        uri = "{0}/{1}".format(COMPUTER_URI, "DEVICE_ID")
        mock_session.get.assert_called_once_with(uri, params=expected_params)

    def test_get_devices_calls_get_expected_number_of_times(
        self, mock_session, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.sdk.settings.items_per_page = 1
        client = DeviceClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in client.get_all():
            pass
        py42.sdk.settings.items_per_page = 1000
        assert mock_session.get.call_count == 3
