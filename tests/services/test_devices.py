import pytest
from requests import HTTPError
from requests import Response
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import pycpg
from pycpg.clients.settings.device_settings import DeviceSettings
from pycpg.exceptions import PycpgActiveLegalHoldError
from pycpg.exceptions import PycpgBadRequestError
from pycpg.exceptions import PycpgOrgNotFoundError
from pycpg.response import PycpgResponse
from pycpg.services.devices import DeviceService

COMPUTER_URI = "/api/v1/Computer"
UPGRADE_URI = "/api/v4/device-upgrade/upgrade-device"

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


class TestDeviceService:
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        yield create_mock_response(mocker, MOCK_GET_DEVICE_RESPONSE)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        yield create_mock_response(mocker, MOCK_EMPTY_GET_DEVICE_RESPONSE)

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
        unicode_hostname = "您已经发现了秘密信息"
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
        uri = f"{COMPUTER_URI}/DEVICE_ID"
        mock_connection.get.assert_called_once_with(uri, params=expected_params)

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_empty_response
    ):
        pycpg.settings.items_per_page = 1
        service = DeviceService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in service.get_all():
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_connection):
        service = DeviceService(mock_connection)
        service.get_page(20, True, True, "org", "user", "dest", True, True, 1000)
        mock_connection.get.assert_called_once_with(
            "/api/v1/Computer",
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
        uri = "/api/v14/agent-state/view-by-device-guid"
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
            if "computer-deactivation" in url:
                base_err = mocker.MagicMock(spec=HTTPError)
                base_err.response = mocker.MagicMock(spec=Response)
                base_err.response.text = "ACTIVE_LEGAL_HOLD"
                raise PycpgBadRequestError(base_err)

        mock_connection.post.side_effect = side_effect
        client = DeviceService(mock_connection)
        with pytest.raises(PycpgActiveLegalHoldError) as err:
            client.deactivate(1234)

        expected = "Cannot deactivate the device with ID 1234 as the device is involved in a legal hold matter."
        assert expected in str(err.value)
        assert err.value.resource == "device"
        assert err.value.resource_id == 1234

    def test_get_page_when_org_not_found_raises_expected_error(
        self, mocker, mock_connection
    ):
        text = '[{"name":"SYSTEM","description":"Unable to find org"}]'
        mock_connection.get.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, text
        )
        service = DeviceService(mock_connection)

        with pytest.raises(PycpgOrgNotFoundError) as err:
            service.get_page(1, org_uid="TestOrgUid")

        assert "The organization with UID 'TestOrgUid' was not found." in str(err.value)
        assert err.value.org_uid == "TestOrgUid"

    def test_upgrade_calls_upgrade_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = DeviceService(mock_connection)
        service.upgrade("DEVICE_ID")
        expected_params = {"deviceGuid": "DEVICE_ID"}
        mock_connection.post.assert_called_once_with(UPGRADE_URI, json=expected_params)

    def test_get_settings_returns_crashplan_settings_when_crashplan_service(
        self, mocker, mock_connection
    ):
        text = """{"service": "Crashplan", "availableDestinations": "", "settings": {"serviceBackupConfig": {"backupConfig": {"backupSets": ""}}}}"""
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = text
        client = DeviceService(mock_connection)
        mock_connection.get.return_value = PycpgResponse(requests_response)
        settings = client.get_settings("42")
        assert isinstance(settings, DeviceSettings)


    def test_update_settings_calls_api_with_expected_params_when_crashplan(
        self, mock_connection
    ):
        device_id = "123"
        device_dict = {
            "computerId": device_id,
            "service": "Crashplan",
            "availableDestinations": "",
            "settings": {
                "configDateMs": "123",
                "serviceBackupConfig": {"backupConfig": {"backupSets": ""}},
            },
        }
        settings = DeviceSettings(device_dict)
        client = DeviceService(mock_connection)
        client.update_settings(settings)
        uri = f"/api/v1/Computer/{device_id}"
        mock_connection.put.assert_called_once_with(uri, json=settings)

   