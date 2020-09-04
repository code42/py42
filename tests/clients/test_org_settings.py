from copy import deepcopy

import pytest
from tests.clients.conftest import param
from tests.clients.conftest import PHOTOS_REGEX
from tests.clients.conftest import PICTURES_REGEX
from tests.clients.conftest import TEST_ADDED_EXCLUDED_PATH
from tests.clients.conftest import TEST_ADDED_PATH
from tests.clients.conftest import TEST_DESTINATION_GUID_1
from tests.clients.conftest import TEST_DESTINATION_GUID_2
from tests.clients.conftest import TEST_DESTINATION_GUID_3
from tests.clients.conftest import TEST_DESTINATION_NAME_1
from tests.clients.conftest import TEST_DESTINATION_NAME_2
from tests.clients.conftest import TEST_DESTINATION_NAME_3
from tests.clients.conftest import TEST_EXTERNAL_DOCUMENTS_DIR
from tests.clients.conftest import TEST_HOME_DIR
from tests.clients.conftest import TEST_PHOTOS_DIR
from tests.clients.test_device_settings import DEVICE_DICT_W_SETTINGS

from py42.clients.settings import get_val
from py42.clients.settings.org_settings import OrgSettings
from py42.exceptions import Py42Error

ONEGB = 1000000000
TEST_ORG_ID = 42
TEST_ORG_NAME = "Test Org"
TEST_REG_KEY = "XXXX-XXXX-XXXX-XXXX"
TEST_NOTE = "Test Note"
TEST_EXTERNAL_REFERENCE = "Test Ref"
TEST_ARCHIVE_HOLD_DAYS = 30
TEST_MAX_SUBSCRIPTIONS = 100
TEST_ORG_QUOTA_BYTES = 1000 * ONEGB
TEST_USER_QUOTA_BYTES = 100 * ONEGB
TEST_WEB_RESTORE_USER_LIMIT = 25
TEST_WEB_RESTORE_ADMIN_LIMIT = 1000
TEST_BACKUP_WARNING_EMAIL_DAYS = 5
TEST_BACKUP_CRITICAL_EMAIL_DAYS = 10

TEST_UNOFFERED_DESTINATION_GUID = "4500"
TEST_UNOFFERED_DESTINATION_NAME = "Dest45"

TEST_ORG_SETTINGS_DICT = {
    "orgId": TEST_ORG_ID,
    "orgUid": "944755074379520217",
    "orgName": TEST_ORG_NAME,
    "orgExtRef": TEST_EXTERNAL_REFERENCE,
    "notes": TEST_NOTE,
    "status": "Active",
    "active": True,
    "blocked": False,
    "parentOrgId": 510853,
    "parentOrgUid": "917669379999168715",
    "type": "ENTERPRISE",
    "classification": "BASIC",
    "externalId": "944755074379520217",
    "hierarchyCounts": {},
    "configInheritanceCounts": {},
    "creationDate": "2020-03-10T13:38:26.222-05:00",
    "modificationDate": "2020-09-01T15:36:35.872-05:00",
    "deactivationDate": None,
    "registrationKey": TEST_REG_KEY,
    "reporting": {"orgManagers": []},
    "customConfig": True,
    "settings": {
        "maxSeats": TEST_MAX_SUBSCRIPTIONS,
        "maxBytes": TEST_ORG_QUOTA_BYTES,
        "archiveHoldDays": TEST_ARCHIVE_HOLD_DAYS,
        "defaultUserMaxBytes": TEST_USER_QUOTA_BYTES,
        "defaultUserMobileQuota": -1,
        "webRestoreUserLimitMb": TEST_WEB_RESTORE_USER_LIMIT,
        "webRestoreAdminLimitMb": TEST_WEB_RESTORE_ADMIN_LIMIT,
        "warnInDays": TEST_BACKUP_WARNING_EMAIL_DAYS,
        "alertInDays": TEST_BACKUP_CRITICAL_EMAIL_DAYS,
        "recipients": [],
        "reportLastSent": None,
        "reportSchedule": "_______",
        "sendReports": False,
        "usernameIsAnEmail": True,
        "ldapServerIds": None,
        "radiusServerIds": None,
        "ssoIdentityProviderUids": None,
        "securityKeyType": "AccountPassword",
        "securityKeyLocked": True,
        "autoOfferSelf": False,
        "allowLocalFolders": True,
        "defaultRoles": [],
        "isSimpleOrg": False,
        "isDefaultRolesInherited": True,
        "destinations": [
            {
                "destinationId": int(TEST_DESTINATION_GUID_1),
                "guid": TEST_DESTINATION_GUID_1,
                "destinationName": TEST_DESTINATION_NAME_1,
                "type": "CLUSTER",
            },
            {
                "destinationId": int(TEST_DESTINATION_GUID_2),
                "guid": TEST_DESTINATION_GUID_2,
                "destinationName": TEST_DESTINATION_NAME_2,
                "type": "CLUSTER",
            },
            {
                "destinationId": int(TEST_DESTINATION_GUID_3),
                "guid": TEST_DESTINATION_GUID_3,
                "destinationName": TEST_DESTINATION_NAME_3,
                "type": "CLUSTER",
            },
        ],
        "allDestinations": [
            {
                "destinationId": int(TEST_DESTINATION_GUID_1),
                "guid": TEST_DESTINATION_GUID_1,
                "destinationName": TEST_DESTINATION_NAME_1,
                "type": "CLUSTER",
            },
            {
                "destinationId": int(TEST_DESTINATION_GUID_2),
                "guid": TEST_DESTINATION_GUID_2,
                "destinationName": TEST_DESTINATION_NAME_2,
                "type": "CLUSTER",
            },
            {
                "destinationId": int(TEST_UNOFFERED_DESTINATION_GUID),
                "guid": TEST_UNOFFERED_DESTINATION_GUID,
                "destinationName": TEST_UNOFFERED_DESTINATION_NAME,
                "type": "CLUSTER",
            },
        ],
        "isUsingDestinationDefaults": True,
        "isUsingQuotaDefaults": False,
        "isUsingReportingDefaults": True,
        "isNativeClientsEnabled": True,
        "securityKeyInherit": True,
    },
    "settingsInherited": {
        "maxSeats": "",
        "maxBytes": "",
        "archiveHoldDays": 21,
        "defaultUserMaxBytes": -1,
        "defaultUserMobileQuota": -1,
        "webRestoreUserLimitMb": 250,
        "webRestoreAdminLimitMb": 250,
        "warnInDays": 7,
        "alertInDays": 14,
        "recipients": [],
        "reportSchedule": "_______",
        "sendReports": False,
        "usernameIsAnEmail": True,
        "ldapServerIds": [0],
        "radiusServerIds": [0],
        "ssoIdentityProviderUids": ["0"],
        "securityKeyType": "AccountPassword",
        "securityKeyLocked": True,
        "autoOfferSelf": False,
        "allowLocalFolders": True,
        "defaultRoles": [],
        "isSimpleOrg": False,
        "destinations": [
            [
                {
                    "destinationId": int(TEST_DESTINATION_GUID_1),
                    "guid": TEST_DESTINATION_GUID_1,
                    "destinationName": TEST_DESTINATION_NAME_1,
                    "type": "CLUSTER",
                },
                {
                    "destinationId": int(TEST_DESTINATION_GUID_2),
                    "guid": TEST_DESTINATION_GUID_2,
                    "destinationName": TEST_DESTINATION_NAME_2,
                    "type": "CLUSTER",
                },
            ],
        ],
    },
    "deviceDefaults": DEVICE_DICT_W_SETTINGS["settings"],
}

TEST_T_SETTINGS_DICT = {
    "device_upgrade_delay": {
        "scope": "ORG",
        "value": "60",
        "locked": False,
        "id": 510808,
    },
    "org-securityTools-device-detection-enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "device_engine_pause_allowedTypes": {
        "scope": "ORG",
        "value": '["legalHold","backup"]',
        "locked": False,
        "id": 537575,
    },
    "device_advancedExfiltrationDetection_enabled": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "org_securityTools_printer_detection_enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "device_network_dscp_preferIP4": {
        "scope": "ORG",
        "value": "false",
        "locked": False,
        "id": 537575,
    },
    "org-securityTools-cloud-detection-enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "org-securityTools-enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "c42.msa.acceptance": {
        "scope": "ORG",
        "value": "917633711460206173;tim.putnam+legacyadmin@code42.com;2019-09-05T17:05:09:046",
        "locked": True,
        "id": 510682,
    },
    "org-securityTools-yara-scanner-enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 510853,
    },
    "org-securityTools-restore-detection-enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 510853,
    },
    "device_fileForensics_enabled": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "device_webRestore_enabled": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 510808,
    },
    "device_network_utilization_schedule_enabled": {
        "scope": "ORG",
        "value": "true",
        "locked": True,
        "id": 537575,
    },
    "device_network_utilization_schedule_rate": {
        "scope": "ORG",
        "value": '{"peak":{"wan":{"active":"256","idle":"0"},"lan":{"active":"256","idle":"256"}},"offPeak":{"wan":{"active":0,"idle":0},"lan":{"active":0,"idle":0}}}',
        "locked": True,
        "id": 537575,
    },
    "org-securityTools-open-file-detection-enable": {
        "scope": "ORG",
        "value": "true",
        "locked": False,
        "id": 537575,
    },
    "device_network_utilization_schedule": {
        "scope": "ORG",
        "value": '{"sun":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"mon":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"tue":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"wed":{"included":true,"startTimeOfDay":"12:00","endTimeOfDay":"19:00"},"thu":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"fri":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"sat":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"}}',
        "locked": True,
        "id": 537575,
    },
}


@pytest.fixture
def org_device_defaults_with_empty_values():
    org_settings_dict = deepcopy(TEST_ORG_SETTINGS_DICT)
    # set empty file selection
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["pathset"] = [{"@cleared": "true", "@os": "Linux"}]
    # set empty filename exclusions
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["excludeUser"] = [
        {u"windows": [], u"linux": [], u"macintosh": []}
    ]
    return org_settings_dict


@pytest.fixture
def org_device_defaults_with_single_values():
    org_settings_dict = deepcopy(TEST_ORG_SETTINGS_DICT)
    # set single path file selection
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["pathset"] = [
        {"path": {"@include": TEST_HOME_DIR}, "@os": "Linux"}
    ]
    # set single filename exclusions
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["excludeUser"] = [
        {
            "windows": [],
            "pattern": {"@regex": PHOTOS_REGEX},
            "linux": [],
            "macintosh": [],
        }
    ]
    return org_settings_dict


@pytest.fixture
def org_device_defaults_with_multiple_values():
    org_settings_dict = deepcopy(TEST_ORG_SETTINGS_DICT)
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["pathset"] = [
        {
            "path": [
                {"@include": TEST_HOME_DIR},
                {"@include": TEST_EXTERNAL_DOCUMENTS_DIR},
                {"@exclude": TEST_PHOTOS_DIR},
            ],
            "@os": "Linux",
        }
    ]
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["excludeUser"] = [
        {
            "windows": [],
            "pattern": [{"@regex": PHOTOS_REGEX}, {"@regex": PICTURES_REGEX}],
            "linux": [],
            "macintosh": [],
        }
    ]
    return org_settings_dict


class TestOrgSettings(object):
    org_settings = OrgSettings(
        deepcopy(TEST_ORG_SETTINGS_DICT), deepcopy(TEST_T_SETTINGS_DICT)
    )

    @pytest.mark.parametrize(
        "param",
        [
            ("org_name", TEST_ORG_NAME),
            ("external_reference", TEST_EXTERNAL_REFERENCE),
            ("notes", TEST_NOTE),
            ("archive_hold_days", TEST_ARCHIVE_HOLD_DAYS),
            ("maximum_user_subscriptions", TEST_MAX_SUBSCRIPTIONS),
            ("org_backup_quota_bytes", TEST_ORG_QUOTA_BYTES),
            ("user_backup_quota_bytes", TEST_USER_QUOTA_BYTES),
            ("web_restore_admin_limit_mb", TEST_WEB_RESTORE_ADMIN_LIMIT),
            ("web_restore_user_limit_mb", TEST_WEB_RESTORE_USER_LIMIT),
            ("backup_warning_email_days", TEST_BACKUP_WARNING_EMAIL_DAYS),
            ("backup_critical_email_days", TEST_BACKUP_CRITICAL_EMAIL_DAYS),
            ("backup_alert_recipient_emails", []),
        ],
    )
    def test_org_settings_properties_retrieve_expected_results(self, param):
        attr, expected = param
        assert getattr(self.org_settings, attr) == expected

    @pytest.mark.parametrize(
        "param",
        [
            (
                "available_destinations",
                {"4200": "Dest42", "4300": "Dest43", "4400": "Dest44"},
            ),
            ("warning_email_enabled", True),
            ("critical_email_enabled", True),
            ("warning_alert_days", 5),
            ("critical_alert_days", 10),
            ("backup_status_email_enabled", False),
            ("backup_status_email_frequency_days", 7),
        ],
    )
    def test_org_settings_device_defaults_retrieve_expected_results(self, param):
        attr, expected = param
        assert getattr(self.org_settings.device_defaults, attr) == expected

    def test_org_settings_endpoint_monitoring_enabled_returns_expected_results(self):
        t_setting = deepcopy(TEST_T_SETTINGS_DICT)
        t_setting["org-securityTools-enable"]["value"] = "true"
        org_settings = OrgSettings(TEST_ORG_SETTINGS_DICT, t_setting)
        assert org_settings.endpoint_monitoring_enabled is True

        t_setting["org-securityTools-enable"]["value"] = "false"
        org_settings = OrgSettings(TEST_ORG_SETTINGS_DICT, t_setting)
        assert org_settings.endpoint_monitoring_enabled is False

    def test_org_settings_set_endpoint_monitoring_enabled_to_true_from_false_creates_expected_packets(
        self,
    ):
        t_setting = deepcopy(TEST_T_SETTINGS_DICT)
        t_setting["org-securityTools-enable"]["value"] = "true"
        org_settings = OrgSettings(TEST_ORG_SETTINGS_DICT, t_setting)
        org_settings.endpoint_monitoring_enabled = False
        assert {
            "key": "org-securityTools-enable",
            "value": "false",
            "locked": False,
        } in org_settings.packets
        assert {
            "key": "device_advancedExfiltrationDetection_enabled",
            "value": "false",
            "locked": False,
        } in org_settings.packets
        assert {
            "key": "org-securityTools-cloud-detection-enable",
            "value": "false",
            "locked": False,
        } in org_settings.packets
        assert {
            "key": "org-securityTools-open-file-detection-enable",
            "value": "false",
            "locked": False,
        } in org_settings.packets
        assert {
            "key": "org-securityTools-device-detection-enable",
            "value": "false",
            "locked": False,
        } in org_settings.packets
        assert len(org_settings.packets) == 5

    def test_org_settings_set_endpoint_monitoring_enabled_to_false_from_true_creates_expected_packets(
        self,
    ):
        t_setting = deepcopy(TEST_T_SETTINGS_DICT)
        t_setting["org-securityTools-enable"]["value"] = "false"
        org_settings = OrgSettings(TEST_ORG_SETTINGS_DICT, t_setting)
        org_settings.endpoint_monitoring_enabled = True
        assert {
            "key": "org-securityTools-enable",
            "value": "true",
            "locked": False,
        } in org_settings.packets
        assert {
            "key": "device_advancedExfiltrationDetection_enabled",
            "value": "true",
            "locked": False,
        } in org_settings.packets
        assert len(org_settings.packets) == 2
        # assert org_settings.packets == [
        #     {"key": "org-securityTools-enable", "value": "true", "locked": False},
        #     {
        #         "key": "device_advancedExfiltrationDetection_enabled",
        #         "value": "true",
        #         "locked": False,
        #     },
        # ]

    @pytest.mark.parametrize(
        "param",
        [
            (
                "endpoint_monitoring_removable_media_enabled",
                "org-securityTools-device-detection-enable",
            ),
            (
                "endpoint_monitoring_cloud_sync_enabled",
                "org-securityTools-cloud-detection-enable",
            ),
            (
                "endpoint_monitoring_browser_and_applications_enabled",
                "org-securityTools-open-file-detection-enable",
            ),
            (
                "endpoint_monitoring_file_metadata_collection_enabled",
                "device_fileForensics_enabled",
            ),
        ],
    )
    def test_org_settings_set_endpoint_monitoring_sub_categories_when_endpoint_monitoring_disabled_sets_endpoint_monitoring_enabled(
        self, param
    ):
        attr, key = param
        t_setting = deepcopy(TEST_T_SETTINGS_DICT)
        t_setting["org-securityTools-enable"]["value"] = "false"
        org_settings = OrgSettings(TEST_ORG_SETTINGS_DICT, t_setting)
        setattr(org_settings, attr, True)
        packet_keys = [packet["key"] for packet in org_settings.packets]
        assert key in packet_keys
        assert "org-securityTools-enable" in packet_keys
        for packet in org_settings.packets:
            if packet["key"] == "org-securityTools-enable":
                assert packet["value"] == "true"
            if packet["key"] == key:
                assert packet["value"] == "true"

    @pytest.mark.parametrize(
        "param",
        [
            param(
                name="org_name",
                new_val="Org Name Updated",
                expected_stored_val="Org Name Updated",
                dict_location=["orgName"],
            ),
            param(
                name="external_reference",
                new_val="Updated Reference",
                expected_stored_val="Updated Reference",
                dict_location=["orgExtRef"],
            ),
            param(
                name="notes",
                new_val="Updated Note",
                expected_stored_val="Updated Note",
                dict_location=["notes"],
            ),
            param(
                name="maximum_user_subscriptions",
                new_val=99,
                expected_stored_val=99,
                dict_location=["settings", "maxSeats"],
            ),
            param(
                name="org_backup_quota_bytes",
                new_val=ONEGB * 42,
                expected_stored_val=ONEGB * 42,
                dict_location=["settings", "maxBytes"],
            ),
            param(
                name="user_backup_quota_bytes",
                new_val=ONEGB * 42,
                expected_stored_val=ONEGB * 42,
                dict_location=["settings", "defaultUserMaxBytes"],
            ),
            param(
                name="web_restore_admin_limit_mb",
                new_val=42,
                expected_stored_val=42,
                dict_location=["settings", "webRestoreAdminLimitMb"],
            ),
            param(
                name="web_restore_user_limit_mb",
                new_val=42,
                expected_stored_val=42,
                dict_location=["settings", "webRestoreUserLimitMb"],
            ),
            param(
                name="backup_warning_email_days",
                new_val=14,
                expected_stored_val=14,
                dict_location=["settings", "warnInDays"],
            ),
            param(
                name="backup_critical_email_days",
                new_val=25,
                expected_stored_val=25,
                dict_location=["settings", "alertInDays"],
            ),
            param(
                name="backup_alert_recipient_emails",
                new_val="test@example.com",  # test string input
                expected_stored_val=["test@example.com"],
                dict_location=["settings", "recipients"],
            ),
            param(
                name="backup_alert_recipient_emails",
                new_val=["test@example.com", "test2@example.com"],  # test list input
                expected_stored_val=["test@example.com", "test2@example.com"],
                dict_location=["settings", "recipients"],
            ),
        ],
    )
    def test_org_settings_setting_mutable_property_updates_dict_correctly_and_registers_changes(
        self,
        param,
    ):
        setattr(self.org_settings, param.name, param.new_val)
        assert (
            get_val(self.org_settings.data, param.dict_location)
            == param.expected_stored_val
        )
        assert param.name in self.org_settings.changes


class TestOrgDeviceSettingsDefaultsBackupSets(object):
    org_settings = OrgSettings(
        deepcopy(TEST_ORG_SETTINGS_DICT), deepcopy(TEST_T_SETTINGS_DICT)
    )

    def test_backup_set_destinations_property_returns_expected_value(
        self,
    ):
        expected_destinations = {"4200": "Dest42 <LOCKED>", "4300": "Dest43"}
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations
        )

    def test_backup_set_add_destination_when_destination_available(
        self,
    ):
        self.org_settings.device_defaults.backup_sets[0].add_destination(4400)
        expected_destinations_property = {
            "4200": "Dest42 <LOCKED>",
            "4300": "Dest43",
            "4400": "Dest44",
        }
        expected_destinations_dict = [
            {"@id": TEST_DESTINATION_GUID_1, "@locked": "true"},
            {"@id": TEST_DESTINATION_GUID_2},
            {"@id": TEST_DESTINATION_GUID_3},
        ]
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"][0]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_add_destination_when_destination_not_available_raises(
        self,
    ):
        expected_destinations_property = {
            "4200": "Dest42 <LOCKED>",
            "4300": "Dest43",
            "4400": "Dest44",
        }
        with pytest.raises(Py42Error):
            self.org_settings.device_defaults.backup_sets[0].add_destination(404)
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations_property
        )

    def test_backup_set_remove_destination_when_destination_available(
        self,
    ):
        expected_destinations_property = {
            "4200": "Dest42 <LOCKED>",
            "4300": "Dest43",
        }
        expected_destinations_dict = [
            {"@id": TEST_DESTINATION_GUID_1, "@locked": "true"},
            {"@id": TEST_DESTINATION_GUID_2},
        ]
        self.org_settings.device_defaults.backup_sets[0].remove_destination(4400)
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"][0]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_remove_destination_when_destination_not_available_raises(
        self,
    ):
        expected_destinations_property = {
            "4200": "Dest42 <LOCKED>",
            "4300": "Dest43",
        }
        with pytest.raises(Py42Error):
            self.org_settings.device_defaults.backup_sets[0].remove_destination(404)
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations_property
        )

    def test_backup_set_lock_destination(self):
        expected_destinations_property = {
            "4200": "Dest42 <LOCKED>",
            "4300": "Dest43 <LOCKED>",
        }
        expected_destinations_dict = [
            {"@id": TEST_DESTINATION_GUID_1, "@locked": "true"},
            {"@id": TEST_DESTINATION_GUID_2, "@locked": "true"},
        ]
        self.org_settings.device_defaults.backup_sets[0].lock_destination(4300)
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"][0]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_unlock_destination(self):
        expected_destinations_property = {
            "4200": "Dest42",
            "4300": "Dest43 <LOCKED>",
        }
        expected_destinations_dict = [
            {"@id": TEST_DESTINATION_GUID_1},
            {"@id": TEST_DESTINATION_GUID_2, "@locked": "true"},
        ]
        self.org_settings.device_defaults.backup_sets[0].unlock_destination(4200)
        assert (
            self.org_settings.device_defaults.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"][0]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_included_files_returns_expected_values(
        self,
        org_device_defaults_with_empty_values,
        org_device_defaults_with_single_values,
        org_device_defaults_with_multiple_values,
    ):
        # empty pathset
        org_settings = OrgSettings(
            org_device_defaults_with_empty_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].included_files == []

        # single path pathset
        org_settings = OrgSettings(
            org_device_defaults_with_single_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].included_files == [
            TEST_HOME_DIR
        ]

        # multiple path pathset
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].included_files == [
            TEST_HOME_DIR,
            TEST_EXTERNAL_DOCUMENTS_DIR,
        ]

    def test_backup_set_included_files_append_produces_expected_pathset_value_and_registers_change(
        self,
    ):
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_EXTERNAL_DOCUMENTS_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
        ]

        self.org_settings.device_defaults.backup_sets[0].included_files.append(
            TEST_ADDED_PATH
        )
        actual_path_list = self.org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "included_files" in self.org_settings.device_defaults.changes
        assert (
            "-> {}".format(
                [TEST_HOME_DIR, TEST_EXTERNAL_DOCUMENTS_DIR, TEST_ADDED_PATH]
            )
            in self.org_settings.device_defaults.changes["included_files"]
        )

    def test_backup_set_included_files_remove_produces_expected_pathset_value(self):
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
        ]

        self.org_settings.device_defaults.backup_sets[0].included_files.remove(
            TEST_EXTERNAL_DOCUMENTS_DIR
        )
        actual_path_list = self.org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "included_files" in self.org_settings.device_defaults.changes
        assert (
            "-> {}".format([TEST_HOME_DIR, TEST_ADDED_PATH])
            in self.org_settings.device_defaults.changes["included_files"]
        )

    def test_backup_set_excluded_files_returns_expected_values(
        self,
        org_device_defaults_with_empty_values,
        org_device_defaults_with_multiple_values,
    ):
        # empty file selection
        org_settings = OrgSettings(
            org_device_defaults_with_empty_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].excluded_files == []

        # multiple path pathset
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].excluded_files == [
            TEST_PHOTOS_DIR
        ]

    def test_backup_set_excluded_files_append_produces_expected_pathset_value_and_registers_change(
        self,
    ):
        self.org_settings.device_defaults.backup_sets[0].excluded_files.append(
            TEST_ADDED_EXCLUDED_PATH
        )
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
            {"@exclude": TEST_ADDED_EXCLUDED_PATH, "@und": "false"},
        ]
        actual_path_list = self.org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "excluded_files" in self.org_settings.device_defaults.changes
        assert (
            "-> {}".format([TEST_PHOTOS_DIR, TEST_ADDED_EXCLUDED_PATH])
            in self.org_settings.device_defaults.changes["excluded_files"]
        )

    def test_backup_set_excluded_files_remove_produces_expected_pathset_value(self):
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_ADDED_EXCLUDED_PATH, "@und": "false"},
        ]
        self.org_settings.device_defaults.backup_sets[0].excluded_files.remove(
            TEST_PHOTOS_DIR
        )
        actual_path_list = self.org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "excluded_files" in self.org_settings.device_defaults.changes
        assert (
            "-> {}".format([TEST_ADDED_EXCLUDED_PATH])
            in self.org_settings.device_defaults.changes["excluded_files"]
        )

    def test_backup_set_filename_exclusions_returns_expected_list_results(
        self,
        org_device_defaults_with_empty_values,
        org_device_defaults_with_single_values,
        org_device_defaults_with_multiple_values,
    ):
        # empty exclude list
        org_settings = OrgSettings(
            org_device_defaults_with_empty_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].filename_exclusions == []

        # single exclude
        org_settings = OrgSettings(
            org_device_defaults_with_single_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].filename_exclusions == [
            PHOTOS_REGEX
        ]

        # multiple excludes
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        assert org_settings.device_defaults.backup_sets[0].filename_exclusions == [
            PHOTOS_REGEX,
            PICTURES_REGEX,
        ]

    def test_backup_set_filename_exclusions_append_produces_expected_values(
        self,
        org_device_defaults_with_empty_values,
        org_device_defaults_with_single_values,
        org_device_defaults_with_multiple_values,
    ):
        # empty starting filename exclusions
        org_settings = OrgSettings(
            org_device_defaults_with_empty_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].filename_exclusions.append(
            PHOTOS_REGEX
        )
        assert org_settings["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX}
        ]
        assert "filename_exclusions" in org_settings.changes
        assert PHOTOS_REGEX in org_settings.changes["filename_exclusions"]

        # single starting filename exclusion
        org_settings = OrgSettings(
            org_device_defaults_with_single_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].filename_exclusions.append(
            PICTURES_REGEX
        )
        assert org_settings["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX},
            {"@regex": PICTURES_REGEX},
        ]
        assert "filename_exclusions" in org_settings.changes
        assert PHOTOS_REGEX in org_settings.changes["filename_exclusions"]
        assert PICTURES_REGEX in org_settings.changes["filename_exclusions"]

        # multiple starting filename exclusions
        NEW_REGEX = ".*/Logs/"
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].filename_exclusions.append(
            NEW_REGEX
        )
        assert org_settings["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX},
            {"@regex": PICTURES_REGEX},
            {"@regex": NEW_REGEX},
        ]
        assert "filename_exclusions" in org_settings.changes
        assert PHOTOS_REGEX in org_settings.changes["filename_exclusions"]
        assert PICTURES_REGEX in org_settings.changes["filename_exclusions"]
        assert NEW_REGEX in org_settings.changes["filename_exclusions"]
