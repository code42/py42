# -*- coding: utf-8 -*-
import pytest

from tests.conftest import py42_response

from requests import HTTPError
from requests import Response

import py42
from py42.exceptions import Py42ActiveLegalHoldError
from py42.exceptions import Py42BadRequestError
from py42.services.devices import DeviceService

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
    "pgSize": 500,
    "q": None,
}

MOCK_GET_DEVICE_RESPONSE = """{"totalCount": 3000, "computers":["foo"]}"""

MOCK_EMPTY_GET_DEVICE_RESPONSE = """{"totalCount": 3000, "computers":[]}"""


class TestDeviceService(object):
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        return py42_response(mocker, MOCK_GET_DEVICE_RESPONSE)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        return py42_response(mocker, MOCK_EMPTY_GET_DEVICE_RESPONSE)

    def test_get_all_calls_get_with_uri_and_params(
        self, mock_connection, mock_get_all_response
    ):
        service = DeviceService(mock_connection)
        mock_connection.get.return_value = mock_get_all_response
        for _ in service.get_all(q="TEST-HOSTNAME"):
            break
        expected_params = DEFAULT_GET_DEVICES_PARAMS
        expected_params["q"] = "TEST-HOSTNAME"
        first_call = mock_connection.get.call_args_list[0]
        assert first_call[0][0] == COMPUTER_URI
        assert first_call[1]["params"] == DEFAULT_GET_DEVICES_PARAMS

    def test_unicode_hostname_get_devices_calls_get_with_unicode_q_param(
        self, mock_connection, mock_get_all_response
    ):
        unicode_hostname = u"您已经发现了秘密信息"
        service = DeviceService(mock_connection)
        mock_connection.get.return_value = mock_get_all_response
        for _ in service.get_all(q=unicode_hostname):
            break
        first_call = mock_connection.get.call_args_list[0]
        assert first_call[0][0] == COMPUTER_URI
        params = DEFAULT_GET_DEVICES_PARAMS
        params["q"] = unicode_hostname
        assert first_call[1]["params"] == params

    def test_get_by_id_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = DeviceService(mock_connection)
        service.get_by_id("DEVICE_ID", include_backup_usage=True)
        expected_params = {"incBackupUsage": True}
        uri = "{}/{}".format(COMPUTER_URI, "DEVICE_ID")
        mock_connection.get.assert_called_once_with(uri, params=expected_params)

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.settings.items_per_page = 1
        service = DeviceService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in service.get_all():
            pass
        py42.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_connection):
        service = DeviceService(mock_connection)
        service.get_page(20, True, True, "org", "user", "dest", True, True, 1000)
        mock_connection.get.assert_called_once_with(
            "/api/Computer",
            params={
                "active": True,
                "blocked": True,
                "orgUid": "org",
                "userUid": "user",
                "targetComputerGuid": "dest",
                "incBackupUsage": True,
                "incCounts": True,
                "pgNum": 20,
                "pgSize": 1000,
                "q": None,
            },
        )

    def test_get_agent_state_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = DeviceService(mock_connection)
        service.get_agent_state("DEVICE_ID", property_name="KEY")
        expected_params = {"deviceGuid": "DEVICE_ID", "propertyName": "KEY"}
        uri = u"/api/v14/agent-state/view-by-device-guid"
        mock_connection.get.assert_called_once_with(uri, params=expected_params)

    def test_get_agent_full_disk_access_state_calls_get_agent_state_with_arguments(
        self, mock_connection, successful_response, mocker
    ):
        mock_connection.get.return_value = successful_response
        service = DeviceService(mock_connection)
        service.get_agent_state = mocker.Mock()
        service.get_agent_full_disk_access_state("DEVICE_ID")
        service.get_agent_state.assert_called_once_with("DEVICE_ID", "fullDiskAccess")

    def test_deactivate_when_user_in_legal_hold_raises_active_legal_hold_error(
        self, mocker, mock_connection
    ):
        def side_effect(url, json):
            if u"computer-deactivation" in url:
                base_err = mocker.MagicMock(spec=HTTPError)
                base_err.response = mocker.MagicMock(spec=Response)
                base_err.response.text = u"ACTIVE_LEGAL_HOLD"
                raise Py42BadRequestError(base_err)

        mock_connection.post.side_effect = side_effect
        client = DeviceService(mock_connection)
        with pytest.raises(Py42ActiveLegalHoldError) as err:
            client.deactivate(1234)

        expected = u"Cannot deactivate the device with ID 1234 as the device is involved in a legal hold matter."
        assert str(err.value) == expected
