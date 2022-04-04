import pytest
from tests.clients.conftest import param

from py42.clients.settings import get_val
from py42.clients.settings.device_settings import IncydrDeviceSettings

TEST_USER_ID = 13548744
TEST_COMPUTER_ID = 4290210
TEST_COMPUTER_GUID = "42000000"
TEST_COMPUTER_ORG_ID = 424242
TEST_DEVICE_VERSION = 4200000000001
TEST_COMPUTER_NAME = "Incydr Settings Test Device"

INCYDR_DEVICE_DICT_W_SETTINGS = {
    "computerId": 4290210,
    "name": "Incydr Settings Test Device",
    "osHostname": "DESKTOP-I2SKEML",
    "guid": "42000000",
    "type": "COMPUTER",
    "status": "Active",
    "active": True,
    "blocked": False,
    "alertState": 0,
    "alertStates": ["OK"],
    "userId": 13548744,
    "userUid": "1010090007721726158",
    "orgId": 424242,
    "orgUid": "985187827481212202",
    "computerExtRef": "ext ref",
    "notes": "My device setting note!",
    "parentComputerId": None,
    "parentComputerGuid": None,
    "lastConnected": "2021-07-22T12:38:54.854Z",
    "osName": "Windows",
    "osVersion": "10.0.19041",
    "osArch": "x86-64",
    "address": "192.168.223.128",
    "remoteAddress": "50.237.14.12",
    "javaVersion": "",
    "modelInfo": "",
    "timeZone": "(UTC-06:00) Central Time (US & Cana",
    "version": 4200000000001,
    "productVersion": "0.0.1",
    "buildVersion": 3531,
    "creationDate": "2021-06-04T14:30:51.392Z",
    "modificationDate": "2021-07-22T12:38:54.854Z",
    "loginDate": "2021-06-04T14:30:51.362Z",
    "service": "Artemis",
    "orgSettings": {"securityKeyLocked": False},
}


class TestIncydrDeviceSettings:
    device_settings = IncydrDeviceSettings(INCYDR_DEVICE_DICT_W_SETTINGS)

    @pytest.mark.parametrize(
        "param",
        [
            ("name", TEST_COMPUTER_NAME),
            ("computer_id", TEST_COMPUTER_ID),
            ("device_id", TEST_COMPUTER_ID),
            ("guid", TEST_COMPUTER_GUID),
            ("user_id", TEST_USER_ID),
            ("org_id", TEST_COMPUTER_ORG_ID),
            ("version", TEST_DEVICE_VERSION),
        ],
    )
    def test_device_settings_properties_return_expected_value_and_cannot_be_changed(
        self, param
    ):
        name, expected_value = param
        assert getattr(self.device_settings, name) == expected_value
        with pytest.raises(AttributeError):
            setattr(self.device_settings, name, expected_value)

    @pytest.mark.parametrize(
        "param",
        [("notes", "My device setting note!"), ("external_reference", "ext ref")],
    )
    def test_device_settings_get_mutable_properties_return_expected_values(self, param):
        name, expected_value = param
        assert getattr(self.device_settings, name) == expected_value

    @pytest.mark.parametrize(
        "param",
        [
            param(
                name="notes",
                new_val="an Incydr device note.",
                expected_stored_val="an Incydr device note.",
                dict_location=["notes"],
            ),
            param(
                name="external_reference",
                new_val="reference#id",
                expected_stored_val="reference#id",
                dict_location=["computerExtRef"],
            ),
        ],
    )
    def test_device_settings_setting_mutable_property_updates_dict_correctly_and_registers_changes(
        self, param
    ):
        setattr(self.device_settings, param.name, param.new_val)
        assert (
            get_val(self.device_settings.data, param.dict_location)
            == param.expected_stored_val
        )
        assert param.name in self.device_settings.changes
