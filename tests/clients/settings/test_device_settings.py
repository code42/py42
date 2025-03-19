from copy import deepcopy

import pytest
from tests.clients.conftest import param

from pycpg.clients.settings import get_val
from pycpg.clients.settings.device_settings import DeviceSettings
from pycpg.exceptions import PycpgError

TEST_USER_ID = 13548744
TEST_COMPUTER_ID = 4290210
TEST_COMPUTER_GUID = 42000000
TEST_COMPUTER_ORG_ID = 424242
TEST_COMPUTER_NAME = "Settings Test Device"
TEST_DESTINATION_GUID_1 = "4200"
TEST_DESTINATION_GUID_2 = "4300"
TEST_DESTINATION_GUID_3 = "4400"
TEST_DESTINATION_NAME_1 = "Dest42"
TEST_DESTINATION_NAME_2 = "Dest43"
TEST_DESTINATION_NAME_3 = "Dest44"
TEST_CONFIG_DATE_MS = "1577858400000"  # Jan 1, 2020
TEST_HOME_DIR = "C:/Users/TestUser/"
TEST_EXTERNAL_DOCUMENTS_DIR = "D:/Documents/"
TEST_PHOTOS_DIR = "C:/Users/TestUser/Pictures/"
TEST_ADDED_PATH = "E:/"
TEST_ADDED_EXCLUDED_PATH = "C:/Users/TestUser/Downloads/"
TEST_DEVICE_VERSION = 1525200006800
PHOTOS_REGEX = ".*/Photos/"
PICTURES_REGEX = ".*/Pictures/"
TEST_NIL_PARAM = {"@nil": True}
TEST_LEGAL_HOLD_BACKUP_SET_ID = "9999"


DEVICE_DICT_W_SETTINGS = {
    "active": True,
    "address": "192.0.0.42:4247",
    "alertState": 0,
    "alertStates": ["OK"],
    "availableDestinations": [
        {
            "destinationId": 1,
            "destinationName": TEST_DESTINATION_NAME_1,
            "guid": TEST_DESTINATION_GUID_1,
            "type": "CLUSTER",
        },
        {
            "destinationId": 2,
            "destinationName": TEST_DESTINATION_NAME_2,
            "guid": TEST_DESTINATION_GUID_2,
            "type": "CLUSTER",
        },
        {
            "destinationId": 3,
            "destinationName": TEST_DESTINATION_NAME_3,
            "guid": TEST_DESTINATION_GUID_3,
            "type": "CLUSTER",
        },
    ],
    "blocked": False,
    "buildVersion": 778,
    "computerExtRef": None,
    "computerId": TEST_COMPUTER_ID,
    "creationDate": "2020-03-31T09:39:31.597-05:00",
    "guid": TEST_COMPUTER_GUID,
    "javaVersion": "11.0.4",
    "lastConnected": "2020-08-27T14:39:16.183-05:00",
    "loginDate": "2020-08-27T14:07:00.621-05:00",
    "modelInfo": None,
    "modificationDate": "2020-08-31T11:34:13.472-05:00",
    "name": TEST_COMPUTER_NAME,
    "notes": None,
    "orgId": TEST_COMPUTER_ORG_ID,
    "orgSettings": {"securityKeyLocked": True},
    "orgUid": "944755074379520217",
    "osArch": "amd64",
    "osHostname": "W10E-X64-FALLCR",
    "osName": "win",
    "osVersion": "10.0.18362",
    "parentComputerGuid": None,
    "parentComputerId": None,
    "productVersion": "8.0.0",
    "remoteAddress": "10.10.10.42",
    "service": "CrashPlan",
    "settings": {
        "@id": "service",
        "@modified": "2020-08-31T14:03:56:323-0500",
        "@version": "13",
        "configDateMs": TEST_CONFIG_DATE_MS,
        "helpNovice": "INTRO",
        "installVersion": "1525200006770",
        "javaMemoryHeapMax": {"@nil": "true"},
        "location": "0.0.0.0:4242",
        "macIOPriority": "IOPOL_THROTTLE",
        "migrationConfig": {
            "migrationCmdLineArgsLoadState": [],
            "migrationCmdLineArgsScanState": [],
            "migrationEnabled": "false",
            "migrationFrequency": "7",
            "migrationToolType": "USMT",
        },
        "orgType": "ENTERPRISE",
        "securityKeyType": "AccountPassword",
        "serviceBackupConfig": {
            "backupConfig": {
                "activeThrottleRate": "20",
                "backupSets": [
                    {
                        "@id": "1",
                        "backupOpenFiles": "true",
                        "backupPaths": {
                            "excludeUser": [
                                {"linux": [], "macintosh": [], "windows": []}
                            ],
                            "lastModified": "1598370521065",
                            "pathset": [
                                {
                                    "@os": "Linux",
                                    "path": [
                                        {"@include": TEST_HOME_DIR},
                                        {"@include": TEST_EXTERNAL_DOCUMENTS_DIR},
                                        {"@exclude": TEST_PHOTOS_DIR},
                                    ],
                                },
                            ],
                        },
                        "backupRunWindow": [
                            {
                                "@always": "true",
                                "@days": "SMTWHFS",
                                "@endTimeOfDay": "06:00",
                                "@startTimeOfDay": "01:00",
                            }
                        ],
                        "compression": "ON",
                        "dataDeDupAutoMaxFileSize": "1073741824",
                        "dataDeDupAutoMaxFileSizeForWan": "0",
                        "dataDeDuplication": "AUTOMATIC",
                        "destinations": [
                            {"@id": TEST_DESTINATION_GUID_1, "@locked": "true"},
                            {"@id": TEST_DESTINATION_GUID_2},
                        ],
                        "encryptionEnabled": "true",
                        "name": "BackupSet 1",
                        "priority": "1",
                        "retentionPolicy": {
                            "backupFrequency": "900000",
                            "keepDeleted": "true",
                            "keepDeletedMinutes": "0",
                            "lastModified": "1268168797613",
                            "versionLastNinetyDaysInterval": "1440",
                            "versionLastWeekInterval": "15",
                            "versionLastYearInterval": "10080",
                            "versionPrevYearsInterval": "43200",
                        },
                        "scanInterval": "86400000",
                        "scanTime": "03:00",
                        "visible": "true",
                        "watchFiles": "true",
                    }
                ],
                "blockArchiveDataFileSize": "4242538496",
                "blockSize": "32768",
                "cachePath": "C:\\ProgramData\\CrashPlan\\cache",
                "checksumBlocksEnabled": "true",
                "checksumIncomingBackupData": "true",
                "checksumIncomingRestoreData": "true",
                "excludeSystem": [{"linux": [], "macintosh": [], "windows": []}],
                "forceFileChannelDuringClose": "false",
                "hostSystemExcludes": [{"linux": [], "macintosh": [], "windows": []}],
                "idleThrottleRate": "80",
                "largeBlockSize": "131072",
                "largeFileBytes": "10485760",
                "maintenanceInterval": "604800000",
                "maintenanceLoadWorkerDelay": "300000",
                "maintenanceLoadWorkerStartupDelay": "60000",
                "manifestPath": "C:\\ProgramData\\CrashPlan\\backupArchives/",
                "noCompressBlockSize": "524288",
                "noCompressionPatterns": [
                    {"linux": [], "macintosh": [], "windows": []}
                ],
                "numBackupWorkers": "4",
                "numCloseWorkers": "10",
                "numMaintenanceWorkers": "1",
                "numReplaceWorkers": "2",
                "numValidateWorkers": "100",
                "reduceEnabled": "true",
                "scrapPercentAllowed": "10",
                "shouldThrottleFFS": {"#text": "true", "@locked": "true"},
                "smallBlockSize": "4096",
                "softDeleteOfFiles": "false",
                "strongBlockCacheLoadFactor": "0.8",
                "strongBlockCacheMaxSize": "30000",
                "verifyBlocksEnabled": "true",
                "verifyBlocksInterval": "2419200000",
                "verifyBlocksLoadFactor": "0.8",
                "verifyRestoreEnabled": "false",
                "veryLargeBlockSize": "524288",
                "veryLargeFileBytes": "1073741824",
                "weakBlockCacheLoadFactor": "0.8",
            },
            "backupFilesLog": [
                {
                    "@append": "true",
                    "@count": "2",
                    "@level": "ALL",
                    "@limit": "26214400",
                    "@pattern": "log/backup_files.log",
                }
            ],
            "backupStatus": "SAFE",
            "backupStatusEmailEnabled": {"#text": "false", "@locked": "true"},
            "backupStatusEmailFreqInMinutes": {"#text": "10080", "@locked": "true"},
            "hiddenFiles": [{"linux": [], "macintosh": [], "windows": []}],
            "highBandwidthRate": "37.5",
            "inboundRunWindow": [
                {
                    "@always": "true",
                    "@days": "SMTWHFS",
                    "@endTimeOfDay": "06:00",
                    "@startTimeOfDay": "01:00",
                }
            ],
            "lanHighBandwidthRate": "1280",
            "lanLowBandwidthRate": "128",
            "lanNetworks": [{"linux": [], "macintosh": [], "windows": []}],
            "lanTcpTrafficClass": "0",
            "lowBandwidthRate": "12.5",
            "minimumBatteryPercent": "20",
            "minutesUntilSevere": "14400",
            "minutesUntilWarning": "7200",
            "networkInterfacesExcluded": [
                {"linux": [], "macintosh": [], "windows": []}
            ],
            "notifyDeliveryTime": "ANY",
            "restoreFilesLog": [
                {
                    "@append": "false",
                    "@count": "1",
                    "@level": "ALL",
                    "@limit": "1073741824",
                    "@pattern": "log/restore_files.log",
                }
            ],
            "severeEmailEnabled": "true",
            "tcpNoDelay": "true",
            "wanNetworks": [{"linux": [], "macintosh": [], "windows": []}],
            "warningEmailEnabled": "true",
            "wirelessNetworksExcluded": [{"linux": [], "macintosh": [], "windows": []}],
        },
        "serviceErrorInterval": "3600000",
        "servicePeerConfig": {
            "authority": {
                "@address": "central.crashplan.com:443",
                "@hideAddress": "true",
                "@lockAddress": "true",
                "@secondaryAddress": "central.crashplan.com:4282",
                "@transportPublicKey": "test_key",
            },
            "centralConfig": {
                "hideDestinationUsageSetting": "false",
                "websiteHost": "https://www.crashplan.com",
            },
            "inboundMessageBufferSize": "2097152",
            "inboundWorkers": "4",
            "lastKnownBuildNumber": "778",
            "lastKnownVersion": "1525200006800",
            "listenForBackup": {"#text": "false", "@locked": "true"},
            "maxConnectAttempts": "2",
            "maxMessageSize": "20971520",
            "outboundMessageBufferSize": "1310720",
            "portMappingEnabled": "true",
            "remotePACFileUrl": {"@nil": "true"},
            "securityProviderCipherId": "0",
            "securityProviderWorkers": "1",
            "siteLocalInboundMessageBufferSize": "1048576",
            "siteLocalOutboundMessageBufferSize": "2621440",
            "socketReceiveBufferSize": {"#text": "-1", "@locked": "true"},
            "socketSendBufferSize": {"#text": "-1", "@locked": "true"},
            "upgradeBuildNumber": {"@nil": "true"},
            "upgradeDelay": "15000",
            "upgradePath": "upgrade",
            "upgradeVersion": {"@nil": "true"},
            "useProxy": {"#text": "false", "@locked": "true"},
        },
        "serviceUIConfig": {
            "autoLogin": "true",
            "autoLoginPasswordHash": "test_hash",
            "locale": {"@nil": "true"},
            "serviceHost": "localhost",
            "servicePort": "4243",
            "showFullFilePath": "false",
        },
        "socialNetworkConfig": {
            "computerConfigs": [
                {
                    "@id": TEST_DESTINATION_GUID_1,
                    "allocatedCapacity": "-1",
                    "guid": TEST_DESTINATION_GUID_1,
                    "manifestPath": {"@nil": "true"},
                    "manifestPathDefault": "false",
                },
                {
                    "@id": TEST_DESTINATION_GUID_2,
                    "allocatedCapacity": "-1",
                    "guid": TEST_DESTINATION_GUID_2,
                    "manifestPath": {"@nil": "true"},
                    "manifestPathDefault": "false",
                },
            ],
            "userConfigs": [
                {
                    "@id": "1",
                    "manifestPath": {"@nil": "true"},
                    "manifestPathDefault": "false",
                    "userId": "1",
                },
                {
                    "@id": "13548744",
                    "manifestPath": {"@nil": "true"},
                    "manifestPathDefault": "false",
                    "userId": "13548744",
                },
            ],
        },
        "systrayOnStartup": "true",
        "userHome": "C:\\Users\\QA",
        "userIdleDelay": "900000",
        "windowsPriorityBoost": "false",
        "windowsPriorityClass": "NORMAL",
    },
    "status": "Active",
    "timeZone": "America/Chicago",
    "type": "COMPUTER",
    "userId": TEST_USER_ID,
    "userUid": "945056771151950748",
    "version": TEST_DEVICE_VERSION,
}


@pytest.fixture
def device_settings_with_empty_values():
    device_settings_dict = deepcopy(DEVICE_DICT_W_SETTINGS)
    # set empty file selection
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["pathset"] = [{"@cleared": "true", "@os": "Linux"}]
    # set empty filename exclusions
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["excludeUser"] = [{"windows": [], "linux": [], "macintosh": []}]
    # set empty destinations
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["destinations"] = {"@cleared": "true"}
    return device_settings_dict


@pytest.fixture
def device_settings_with_single_values():
    device_settings_dict = deepcopy(DEVICE_DICT_W_SETTINGS)
    # set single path file selection
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["pathset"] = [
        {"path": {"@include": TEST_HOME_DIR}, "@os": "Linux"}
    ]
    # set single filename exclusions
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["excludeUser"] = [
        {
            "windows": [],
            "pattern": {"@regex": PHOTOS_REGEX},
            "linux": [],
            "macintosh": [],
        }
    ]
    return device_settings_dict


@pytest.fixture
def device_settings_with_multiple_values():
    device_settings_dict = deepcopy(DEVICE_DICT_W_SETTINGS)
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
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

    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["backupPaths"]["excludeUser"] = [
        {
            "windows": [],
            "pattern": [{"@regex": PHOTOS_REGEX}, {"@regex": PICTURES_REGEX}],
            "linux": [],
            "macintosh": [],
        }
    ]
    return device_settings_dict


@pytest.fixture
def device_settings_with_locked_backup_set():
    device_settings_dict = deepcopy(DEVICE_DICT_W_SETTINGS)
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ][0]["@locked"] = "true"
    return device_settings_dict


@pytest.fixture
def device_settings_legal_hold():
    legal_hold_bs = {
        "@id": TEST_LEGAL_HOLD_BACKUP_SET_ID,
        "backupOpenFiles": "true",
        "backupPaths": {
            "excludeUser": [{"linux": [], "macintosh": [], "windows": []}],
            "lastModified": "1598370521065",
            "pathset": [
                {
                    "@os": "Linux",
                    "path": [
                        {"@include": TEST_HOME_DIR},
                        {"@include": TEST_EXTERNAL_DOCUMENTS_DIR},
                        {"@exclude": TEST_PHOTOS_DIR},
                    ],
                },
            ],
        },
        "backupRunWindow": [
            {
                "@always": "true",
                "@days": "SMTWHFS",
                "@endTimeOfDay": "06:00",
                "@startTimeOfDay": "01:00",
            }
        ],
        "compression": "ON",
        "dataDeDupAutoMaxFileSize": "1073741824",
        "dataDeDupAutoMaxFileSizeForWan": "0",
        "dataDeDuplication": "AUTOMATIC",
        "destinations": {
            "@locked": "true",
            "destination": [
                {"@id": TEST_DESTINATION_GUID_1, "@locked": "true"},
                {"@id": TEST_DESTINATION_GUID_2, "@locked": "true"},
            ],
        },
        "encryptionEnabled": "true",
        "name": "BackupSet 1",
        "priority": "1",
        "retentionPolicy": {
            "backupFrequency": "900000",
            "keepDeleted": "true",
            "keepDeletedMinutes": "0",
            "lastModified": "1268168797613",
            "versionLastNinetyDaysInterval": "1440",
            "versionLastWeekInterval": "15",
            "versionLastYearInterval": "10080",
            "versionPrevYearsInterval": "43200",
        },
        "scanInterval": "86400000",
        "scanTime": "03:00",
        "visible": "true",
        "watchFiles": "true",
    }
    device_settings_dict = deepcopy(DEVICE_DICT_W_SETTINGS)
    device_settings_dict["settings"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ].insert(0, legal_hold_bs)
    return device_settings_dict


class TestDeviceSettings:
    device_settings = DeviceSettings(DEVICE_DICT_W_SETTINGS)

    @pytest.mark.parametrize(
        "param",
        [
            ("computer_id", TEST_COMPUTER_ID),
            ("guid", TEST_COMPUTER_GUID),
            ("user_id", TEST_USER_ID),
            ("org_id", TEST_COMPUTER_ORG_ID),
            ("version", TEST_DEVICE_VERSION),
            (
                "available_destinations",
                {
                    TEST_DESTINATION_GUID_1: TEST_DESTINATION_NAME_1,
                    TEST_DESTINATION_GUID_2: TEST_DESTINATION_NAME_2,
                    TEST_DESTINATION_GUID_3: TEST_DESTINATION_NAME_3,
                },
            ),
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
        [
            ("notes", None),
            ("name", TEST_COMPUTER_NAME),
            ("external_reference", None),
            ("warning_email_enabled", True),
            ("critical_email_enabled", True),
            ("warning_alert_days", 5),
            ("critical_alert_days", 10),
            ("backup_status_email_enabled", False),
            ("backup_status_email_frequency_days", 7),
        ],
    )
    def test_device_settings_get_mutable_properties_return_expected_values(self, param):
        name, expected_value = param
        assert getattr(self.device_settings, name) == expected_value

    @pytest.mark.parametrize(
        "param",
        [
            param(
                name="notes",
                new_val="a device note.",
                expected_stored_val="a device note.",
                dict_location=["notes"],
            ),
            param(
                name="name",
                new_val="Settings Test Device Updated",
                expected_stored_val="Settings Test Device Updated",
                dict_location=["name"],
            ),
            param(
                name="external_reference",
                new_val="reference#id",
                expected_stored_val="reference#id",
                dict_location=["computerExtRef"],
            ),
            param(
                name="warning_email_enabled",
                new_val=False,
                expected_stored_val="false",
                dict_location=[
                    "settings",
                    "serviceBackupConfig",
                    "warningEmailEnabled",
                ],
            ),
            param(
                name="critical_email_enabled",
                new_val=False,
                expected_stored_val="false",
                dict_location=["settings", "serviceBackupConfig", "severeEmailEnabled"],
            ),
            param(
                name="warning_alert_days",
                new_val=10,
                expected_stored_val="14400",
                dict_location=[
                    "settings",
                    "serviceBackupConfig",
                    "minutesUntilWarning",
                ],
            ),
            param(
                name="critical_alert_days",
                new_val=100,
                expected_stored_val="144000",
                dict_location=["settings", "serviceBackupConfig", "minutesUntilSevere"],
            ),
        ],
    )
    def test_device_settings_setting_mutable_property_updates_dict_correctly_and_registers_changes(
        self,
        param,
    ):
        setattr(self.device_settings, param.name, param.new_val)
        assert (
            get_val(self.device_settings.data, param.dict_location)
            == param.expected_stored_val
        )
        assert param.name in self.device_settings.changes

    @pytest.mark.parametrize(
        "param",
        [
            param(
                name="backup_status_email_frequency_days",
                new_val=9,
                expected_stored_val={"#text": "12960", "@locked": "true"},
                dict_location=[
                    "settings",
                    "serviceBackupConfig",
                    "backupStatusEmailFreqInMinutes",
                ],
            ),
            param(
                name="backup_status_email_enabled",
                new_val=True,
                expected_stored_val={"#text": "true", "@locked": "true"},
                dict_location=[
                    "settings",
                    "serviceBackupConfig",
                    "backupStatusEmailEnabled",
                ],
            ),
        ],
    )
    def test_device_settings_setting_mutable_property_updates_dict_correctly_and_registers_changes_when_setting_locked(
        self,
        param,
    ):
        setattr(self.device_settings, param.name, param.new_val)
        assert (
            get_val(self.device_settings.data, param.dict_location)
            == param.expected_stored_val
        )
        assert param.name in self.device_settings.changes

    def test_device_settings_property_with_nil_true_structure_returns_correctly(self):
        assert self.device_settings.java_memory_heap_max == {"@nil": "true"}


class TestDeviceSettingsBackupSets:
    device_settings = DeviceSettings(deepcopy(DEVICE_DICT_W_SETTINGS))

    def test_backup_set_destinations_property_returns_expected_value(
        self,
    ):
        expected_destinations = {"4200": "Dest42 <LOCKED>", "4300": "Dest43"}
        assert self.device_settings.backup_sets[0].destinations == expected_destinations

    def test_backup_set_add_destination_when_destination_available(
        self,
    ):
        self.device_settings.backup_sets[0].add_destination(4400)
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
            self.device_settings.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
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
        with pytest.raises(PycpgError):
            self.device_settings.backup_sets[0].add_destination(404)
        assert (
            self.device_settings.backup_sets[0].destinations
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
        self.device_settings.backup_sets[0].remove_destination(4400)
        assert (
            self.device_settings.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_remove_destination_when_destination_not_available_raises(
        self,
    ):
        expected_destinations_property = {
            "4200": "Dest42 <LOCKED>",
            "4300": "Dest43",
        }
        with pytest.raises(PycpgError):
            self.device_settings.backup_sets[0].remove_destination(404)
        assert (
            self.device_settings.backup_sets[0].destinations
            == expected_destinations_property
        )

    def test_backup_set_remove_all_destinations_sets_expected_cleared_dict(self):
        expected_empty_destination_dict = {"@cleared": "true"}
        self.device_settings.backup_sets[0].remove_destination(4200)
        self.device_settings.backup_sets[0].remove_destination(4300)
        assert self.device_settings.backup_sets[0].destinations == {}
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
            == expected_empty_destination_dict
        )

    def test_backup_set_add_destination_from_empty_state_converts_cleared_dict_to_destination_list(
        self,
    ):
        expected_empty_destination_dict = {"@cleared": "true"}
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
            == expected_empty_destination_dict
        )
        expected_destinations_property = {
            "4200": "Dest42",
            "4300": "Dest43",
        }
        expected_destinations_dict = [
            {"@id": TEST_DESTINATION_GUID_1},
            {"@id": TEST_DESTINATION_GUID_2},
        ]
        self.device_settings.backup_sets[0].add_destination(4200)
        self.device_settings.backup_sets[0].add_destination(4300)
        assert (
            self.device_settings.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
            == expected_destinations_dict
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
        self.device_settings.backup_sets[0].lock_destination(4200)
        self.device_settings.backup_sets[0].lock_destination(4300)
        assert (
            self.device_settings.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
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
        self.device_settings.backup_sets[0].unlock_destination(4200)
        assert (
            self.device_settings.backup_sets[0].destinations
            == expected_destinations_property
        )
        assert (
            self.device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ][0]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_included_files_returns_expected_values(
        self,
        device_settings_with_empty_values,
        device_settings_with_single_values,
        device_settings_with_multiple_values,
    ):
        # empty pathset
        device_settings = DeviceSettings(device_settings_with_empty_values)
        assert device_settings.backup_sets[0].included_files == []

        # single path pathset
        device_settings = DeviceSettings(device_settings_with_single_values)
        assert device_settings.backup_sets[0].included_files == [TEST_HOME_DIR]

        # multiple path pathset
        device_settings = DeviceSettings(device_settings_with_multiple_values)
        assert device_settings.backup_sets[0].included_files == [
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

        self.device_settings.backup_sets[0].included_files.append(TEST_ADDED_PATH)
        actual_path_list = self.device_settings["settings"]["serviceBackupConfig"][
            "backupConfig"
        ]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "included_files" in self.device_settings.changes

    def test_backup_set_included_files_remove_produces_expected_pathset_value(self):
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
        ]

        self.device_settings.backup_sets[0].included_files.remove(
            TEST_EXTERNAL_DOCUMENTS_DIR
        )
        actual_path_list = self.device_settings["settings"]["serviceBackupConfig"][
            "backupConfig"
        ]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "included_files" in self.device_settings.changes

    def test_backup_set_excluded_files_returns_expected_values(
        self, device_settings_with_empty_values, device_settings_with_multiple_values
    ):
        # empty file selection
        device_settings = DeviceSettings(device_settings_with_empty_values)
        assert device_settings.backup_sets[0].excluded_files == []

        # multiple path pathset
        device_settings = DeviceSettings(device_settings_with_multiple_values)
        assert device_settings.backup_sets[0].excluded_files == [TEST_PHOTOS_DIR]

    def test_backup_set_excluded_files_append_produces_expected_pathset_value_and_registers_change(
        self,
    ):
        self.device_settings.backup_sets[0].excluded_files.append(
            TEST_ADDED_EXCLUDED_PATH
        )
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
            {"@exclude": TEST_ADDED_EXCLUDED_PATH, "@und": "false"},
        ]
        actual_path_list = self.device_settings["settings"]["serviceBackupConfig"][
            "backupConfig"
        ]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "excluded_files" in self.device_settings.changes

    def test_backup_set_excluded_files_remove_produces_expected_pathset_value(self):
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_ADDED_EXCLUDED_PATH, "@und": "false"},
        ]
        self.device_settings.backup_sets[0].excluded_files.remove(TEST_PHOTOS_DIR)
        actual_path_list = self.device_settings["settings"]["serviceBackupConfig"][
            "backupConfig"
        ]["backupSets"][0]["backupPaths"]["pathset"]["paths"]["path"]
        assert actual_path_list == expected_path_list
        assert "excluded_files" in self.device_settings.changes

    def test_backup_set_filename_exclusions_returns_expected_list_results(
        self,
        device_settings_with_empty_values,
        device_settings_with_single_values,
        device_settings_with_multiple_values,
    ):
        # empty exclude list
        device_settings = DeviceSettings(device_settings_with_empty_values)
        assert device_settings.backup_sets[0].filename_exclusions == []

        # single exclude
        device_settings = DeviceSettings(device_settings_with_single_values)
        assert device_settings.backup_sets[0].filename_exclusions == [PHOTOS_REGEX]

        # multiple excludes
        device_settings = DeviceSettings(device_settings_with_multiple_values)
        assert device_settings.backup_sets[0].filename_exclusions == [
            PHOTOS_REGEX,
            PICTURES_REGEX,
        ]

    def test_backup_set_filename_exclusions_append_produces_expected_values(
        self,
        device_settings_with_empty_values,
        device_settings_with_single_values,
        device_settings_with_multiple_values,
    ):
        # empty starting filename exclusions
        device_settings = DeviceSettings(device_settings_with_empty_values)
        device_settings.backup_sets[0].filename_exclusions.append(PHOTOS_REGEX)
        assert device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX}
        ]
        assert "filename_exclusions" in device_settings.changes
        assert PHOTOS_REGEX in device_settings.changes["filename_exclusions"]

        # single starting filename exclusion
        device_settings = DeviceSettings(device_settings_with_single_values)
        device_settings.backup_sets[0].filename_exclusions.append(PICTURES_REGEX)
        assert device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX},
            {"@regex": PICTURES_REGEX},
        ]
        assert "filename_exclusions" in device_settings.changes
        assert PHOTOS_REGEX in device_settings.changes["filename_exclusions"]
        assert PICTURES_REGEX in device_settings.changes["filename_exclusions"]

        # multiple starting filename exclusions
        NEW_REGEX = ".*/Logs/"
        device_settings = DeviceSettings(device_settings_with_multiple_values)
        device_settings.backup_sets[0].filename_exclusions.append(NEW_REGEX)
        assert device_settings["settings"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX},
            {"@regex": PICTURES_REGEX},
            {"@regex": NEW_REGEX},
        ]

    def test_backup_set_when_locked_returns_expected_property_value(
        self, device_settings_with_locked_backup_set
    ):
        device_settings = DeviceSettings(device_settings_with_locked_backup_set)
        assert device_settings.backup_sets[0].locked

    def test_backup_set_when_set_locked_non_destination_attributes_raise_attr_error_when_set(
        self, device_settings_with_locked_backup_set
    ):
        device_settings = DeviceSettings(device_settings_with_locked_backup_set)
        with pytest.raises(AttributeError):
            device_settings.backup_sets[0].included_files.append("test")

        with pytest.raises(AttributeError):
            device_settings.backup_sets[0].included_files = ["test"]

        with pytest.raises(AttributeError):
            device_settings.backup_sets[0].excluded_files.append("test")

        with pytest.raises(AttributeError):
            device_settings.backup_sets[0].excluded_files = ["test"]

        with pytest.raises(AttributeError):
            device_settings.backup_sets[0].filename_exclusions.append("test")

        with pytest.raises(AttributeError):
            device_settings.backup_sets[0].filename_exclusions = ["test"]

    def test_backup_set_when_set_locked_allows_destination_modifications(
        self, device_settings_with_locked_backup_set
    ):
        device_settings = DeviceSettings(device_settings_with_locked_backup_set)
        destination_guid_to_add = list(device_settings.available_destinations)[2]
        destination_guid_to_remove = list(device_settings.available_destinations)[0]
        device_settings.backup_sets[0].add_destination(destination_guid_to_add)
        device_settings.backup_sets[0].remove_destination(destination_guid_to_remove)
        assert destination_guid_to_add in device_settings.backup_sets[0].destinations
        assert (
            destination_guid_to_remove
            not in device_settings.backup_sets[0].destinations
        )

    def test_backup_set_when_device_on_legal_hold_hides_legal_hold_set(
        self, device_settings_legal_hold
    ):
        device_settings = DeviceSettings(device_settings_legal_hold)
        assert len(device_settings.backup_sets) == 1
        for bs in device_settings.backup_sets:
            assert bs["@id"] != TEST_LEGAL_HOLD_BACKUP_SET_ID
