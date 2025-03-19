import json
from copy import deepcopy

import pytest
from tests.clients.conftest import param
from tests.clients.conftest import PHOTOS_REGEX
from tests.clients.conftest import PICTURES_REGEX
from tests.clients.conftest import TEST_ADDED_EXCLUDED_PATH
from tests.clients.conftest import TEST_ADDED_PATH
from tests.clients.conftest import TEST_EXTERNAL_DOCUMENTS_DIR
from tests.clients.conftest import TEST_HOME_DIR
from tests.clients.conftest import TEST_PHOTOS_DIR

from pycpg.clients.settings import get_val
from pycpg.clients.settings.org_settings import OrgSettings
from pycpg.exceptions import PycpgError

ONEGB = 1000000000

TEST_T_SETTINGS_DICT = {
    "device_upgrade_delay": {
        "scope": "ORG",
        "value": "60",
        "locked": False,
        "id": 510808,
    },
    "device_network_dscp_preferIP4": {
        "scope": "ORG",
        "value": "false",
        "locked": False,
        "id": 537575,
    },
    "cpg.msa.acceptance": {
        "scope": "ORG",
        "value": "917633711460206173;tim.putnam+legacyadmin@crashPlan.com;2019-09-05T17:05:09:046",
        "locked": True,
        "id": 510682,
    },
    "device_webRestore_enabled": {
        "scope": "ORG",
        "value": "false",
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
    "device_network_utilization_schedule": {
        "scope": "ORG",
        "value": '{"sun":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"mon":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"tue":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"wed":{"included":true,"startTimeOfDay":"12:00","endTimeOfDay":"19:00"},"thu":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"fri":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"},"sat":{"included":"true","startTimeOfDay":"09:00","endTimeOfDay":"17:00"}}',
        "locked": True,
        "id": 537575,
    },
}


@pytest.fixture
def org_settings_dict():
    with open("tests/clients/settings/org_settings_not_inherited.json") as f:
        data = json.load(f)
    return data["data"]


@pytest.fixture
def org_settings_inherited_dict():
    with open("tests/clients/settings/org_settings_inherited.json") as f:
        data = json.load(f)
    return data["data"]


@pytest.fixture
def org_device_defaults_with_empty_values(org_settings_dict):
    org_settings_dict = deepcopy(org_settings_dict)
    # set empty file selection
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ]["backupSet"][0]["backupPaths"]["pathset"] = [
        {"paths": {"@os": "Linux", "path": [], "@cleared": "true"}}
    ]
    # set empty filename exclusions
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ]["backupSet"][0]["backupPaths"]["excludeUser"] = [
        {"windows": [], "linux": [], "macintosh": []}
    ]
    return org_settings_dict


@pytest.fixture
def org_device_defaults_with_single_values(org_settings_dict):
    org_settings_dict = deepcopy(org_settings_dict)
    # set single path file selection
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ]["backupSet"][0]["backupPaths"]["pathset"] = [
        {"path": {"@include": TEST_HOME_DIR}, "@os": "Linux"}
    ]
    # set single filename exclusions
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ]["backupSet"][0]["backupPaths"]["excludeUser"] = [
        {
            "windows": [],
            "pattern": {"@regex": PHOTOS_REGEX},
            "linux": [],
            "macintosh": [],
        }
    ]
    return org_settings_dict


@pytest.fixture
def org_device_defaults_with_multiple_values(org_settings_dict):
    org_settings_dict = deepcopy(org_settings_dict)
    org_settings_dict["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
        "backupSets"
    ]["backupSet"][0]["backupPaths"]["pathset"] = [
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
    ]["backupSet"][0]["backupPaths"]["excludeUser"] = [
        {
            "windows": [],
            "pattern": [{"@regex": PHOTOS_REGEX}, {"@regex": PICTURES_REGEX}],
            "linux": [],
            "macintosh": [],
        }
    ]
    return org_settings_dict


class TestOrgSettings:
    @pytest.mark.parametrize(
        "param",
        [
            ("org_name", "TEST_ORG"),
            ("external_reference", "test_ref"),
            ("notes", "test_note"),
            ("archive_hold_days", 365),
            ("maximum_user_subscriptions", 99),
            ("org_backup_quota", -1),
            ("user_backup_quota", -1),
            ("web_restore_admin_limit", 500),
            ("web_restore_user_limit", 250),
            ("backup_warning_email_days", 3),
            ("backup_critical_email_days", 14),
            ("backup_alert_recipient_emails", ["test@example.com"]),
        ],
    )
    def test_org_settings_properties_retrieve_expected_results(
        self, param, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        attr, expected = param
        assert getattr(org_settings, attr) == expected

    def test_inherited_org_settings_inheritance_flags_return_true(
        self, org_settings_inherited_dict
    ):
        org_settings = OrgSettings(org_settings_inherited_dict, TEST_T_SETTINGS_DICT)
        assert org_settings.quota_settings_inherited
        assert org_settings.reporting_settings_inherited

    @pytest.mark.parametrize(
        "param",
        [
            ("archive_hold_days", 14),
            ("maximum_user_subscriptions", -1),
            ("org_backup_quota", -1),
            ("user_backup_quota", -1),
            ("web_restore_admin_limit", 250),
            ("web_restore_user_limit", 250),
            ("backup_warning_email_days", 7),
            ("backup_critical_email_days", 14),
            ("backup_alert_recipient_emails", []),
        ],
    )
    def test_inherited_org_settings_properties_retrieve_expected_results(
        self, param, org_settings_inherited_dict
    ):
        org_settings = OrgSettings(org_settings_inherited_dict, TEST_T_SETTINGS_DICT)
        attr, expected = param
        assert getattr(org_settings, attr) == expected

    @pytest.mark.parametrize(
        "param",
        [
            ("archive_hold_days", 15),
            ("maximum_user_subscriptions", 100),
            ("org_backup_quota", 10000),
            ("user_backup_quota", 10000),
        ],
    )
    def test_inherited_org_quota_settings_setattr_removes_inheritance(
        self, param, org_settings_inherited_dict
    ):
        org_settings = OrgSettings(org_settings_inherited_dict, TEST_T_SETTINGS_DICT)
        attr, val = param
        setattr(org_settings, attr, val)
        assert not org_settings.quota_settings_inherited

    @pytest.mark.parametrize(
        "param",
        [
            (
                "available_destinations",
                {
                    "632540230984925185": "PROe Cloud, US - West",
                    "43": "PROe Cloud, US",
                    "673679195225718785": "PROe Cloud, AMS",
                    "587738803578339329": "PROe Cloud, SIN",
                },
            ),
            ("warning_email_enabled", False),
            ("critical_email_enabled", False),
            ("warning_alert_days", 3),
            ("critical_alert_days", 5),
            ("backup_status_email_enabled", False),
            ("backup_status_email_frequency_days", 7),
        ],
    )
    def test_org_settings_device_defaults_retrieve_expected_results(
        self, param, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        attr, expected = param
        assert getattr(org_settings.device_defaults, attr) == expected

    def test_org_settings_set_independent_t_setting_properties(
        self, param, org_settings_dict
    ):
        t_setting = deepcopy(TEST_T_SETTINGS_DICT)
        settings = deepcopy(org_settings_dict)
        org_settings = OrgSettings(settings, t_setting)

        setattr(org_settings, param.name, param.new_val)
        packet_keys = [packet["key"] for packet in org_settings.packets]
        assert param.dict_location in packet_keys
        for packet in org_settings.packets:
            if packet["key"] == param.dict_location:
                assert packet["value"] == "true"

        setattr(org_settings, param.name, False)
        packet_keys = [packet["key"] for packet in org_settings.packets]
        assert param.dict_location in packet_keys
        for packet in org_settings.packets:
            if packet["key"] == param.dict_location:
                assert packet["value"] == "false"
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
                name="org_backup_quota",
                new_val=42,
                expected_stored_val=ONEGB * 42,
                dict_location=["settings", "maxBytes"],
            ),
            param(
                name="user_backup_quota",
                new_val=42,
                expected_stored_val=ONEGB * 42,
                dict_location=["settings", "defaultUserMaxBytes"],
            ),
            param(
                name="web_restore_admin_limit",
                new_val=42,
                expected_stored_val=42,
                dict_location=["settings", "webRestoreAdminLimitMb"],
            ),
            param(
                name="web_restore_user_limit",
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
                new_val="test2@example.com",  # test string input
                expected_stored_val=["test2@example.com"],
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
        self, param, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        setattr(org_settings, param.name, param.new_val)
        assert (
            get_val(org_settings.data, param.dict_location) == param.expected_stored_val
        )
        assert param.name in org_settings.changes


class TestOrgDeviceSettingsDefaultsBackupSets:
    def test_backup_set_destinations_property_returns_expected_value(
        self, org_settings_dict
    ):
        backup_set_0_expected_destinations = {}
        backup_set_1_expected_destinations = {
            "43": "PROe Cloud, US <LOCKED>",
            "673679195225718785": "PROe Cloud, AMS",
        }
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        assert (
            org_settings.device_defaults.backup_sets[0].destinations
            == backup_set_0_expected_destinations
        )
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == backup_set_1_expected_destinations
        )

    def test_backup_set_add_destination_when_destination_available(
        self, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        org_settings.device_defaults.backup_sets[1].add_destination(632540230984925185)
        expected_destinations_property = {
            "43": "PROe Cloud, US <LOCKED>",
            "673679195225718785": "PROe Cloud, AMS",
            "632540230984925185": "PROe Cloud, US - West",
        }
        expected_destinations_list = [
            {"@id": "43", "@locked": "true"},
            {"@id": "673679195225718785"},
            {"@id": "632540230984925185"},
        ]
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == expected_destinations_property
        )
        assert (
            org_settings.device_defaults.backup_sets[1]["destinations"]
            == expected_destinations_list
        )

    def test_backup_set_add_destination_when_destination_not_available_raises(
        self, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        expected_destinations_property = {
            "43": "PROe Cloud, US <LOCKED>",
            "673679195225718785": "PROe Cloud, AMS",
        }
        with pytest.raises(PycpgError):
            org_settings.device_defaults.backup_sets[1].add_destination(404)
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == expected_destinations_property
        )

    def test_backup_set_remove_destination_when_destination_available(
        self, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        expected_destinations_property = {"673679195225718785": "PROe Cloud, AMS"}
        expected_destinations_dict = [{"@id": "673679195225718785"}]
        org_settings.device_defaults.backup_sets[1].remove_destination(43)
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == expected_destinations_property
        )
        assert (
            org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"]["backupSet"][1]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_remove_destination_when_destination_not_available_raises(
        self, org_settings_dict
    ):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        expected_destinations_property = {
            "43": "PROe Cloud, US <LOCKED>",
            "673679195225718785": "PROe Cloud, AMS",
        }
        with pytest.raises(PycpgError):
            org_settings.device_defaults.backup_sets[1].remove_destination(404)
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == expected_destinations_property
        )

    def test_backup_set_lock_destination(self, org_settings_dict):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        expected_destinations_property = {
            "43": "PROe Cloud, US <LOCKED>",
            "673679195225718785": "PROe Cloud, AMS <LOCKED>",
        }
        expected_destinations_dict = [
            {"@id": "43", "@locked": "true"},
            {"@id": "673679195225718785", "@locked": "true"},
        ]
        org_settings.device_defaults.backup_sets[1].lock_destination(673679195225718785)
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == expected_destinations_property
        )
        assert (
            org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"]["backupSet"][1]["destinations"]
            == expected_destinations_dict
        )

    def test_backup_set_unlock_destination(self, org_settings_dict):
        org_settings = OrgSettings(org_settings_dict, TEST_T_SETTINGS_DICT)
        expected_destinations_property = {
            "43": "PROe Cloud, US",
            "673679195225718785": "PROe Cloud, AMS",
        }
        expected_destinations_dict = [
            {"@id": "43"},
            {"@id": "673679195225718785"},
        ]
        org_settings.device_defaults.backup_sets[1].unlock_destination(43)
        assert (
            org_settings.device_defaults.backup_sets[1].destinations
            == expected_destinations_property
        )
        assert (
            org_settings.device_defaults["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"]["backupSet"][1]["destinations"]
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
        self, org_device_defaults_with_multiple_values
    ):
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@include": TEST_EXTERNAL_DOCUMENTS_DIR, "@und": "false"},
            {"@include": TEST_ADDED_PATH, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
        ]

        org_settings.device_defaults.backup_sets[0].included_files.append(
            TEST_ADDED_PATH
        )
        actual_path_list = org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"]["backupSet"][0]["backupPaths"]["pathset"][
            "paths"
        ][
            "path"
        ]
        assert actual_path_list == expected_path_list
        assert "included_files" in org_settings.device_defaults.changes
        assert (
            "-> {}".format(
                [TEST_HOME_DIR, TEST_EXTERNAL_DOCUMENTS_DIR, TEST_ADDED_PATH]
            )
            in org_settings.device_defaults.changes["included_files"]
        )

    def test_backup_set_included_files_remove_produces_expected_pathset_value(
        self, org_device_defaults_with_multiple_values
    ):
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
        ]

        org_settings.device_defaults.backup_sets[0].included_files.remove(
            TEST_EXTERNAL_DOCUMENTS_DIR
        )
        actual_path_list = org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"]["backupSet"][0]["backupPaths"]["pathset"][
            "paths"
        ][
            "path"
        ]
        assert actual_path_list == expected_path_list
        assert "included_files" in org_settings.device_defaults.changes
        assert (
            "-> {}".format([TEST_HOME_DIR])
            in org_settings.device_defaults.changes["included_files"]
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
        self, org_device_defaults_with_multiple_values
    ):
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        org_settings.device_defaults.backup_sets[0].excluded_files.append(
            TEST_ADDED_EXCLUDED_PATH
        )
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
            {"@exclude": TEST_PHOTOS_DIR, "@und": "false"},
            {"@exclude": TEST_ADDED_EXCLUDED_PATH, "@und": "false"},
        ]
        actual_path_list = org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"]["backupSet"][0]["backupPaths"]["pathset"][
            "paths"
        ][
            "path"
        ]
        for path in expected_path_list:
            assert path in actual_path_list
        assert "excluded_files" in org_settings.device_defaults.changes
        assert (
            "-> {}".format([TEST_PHOTOS_DIR, TEST_ADDED_EXCLUDED_PATH])
            in org_settings.device_defaults.changes["excluded_files"]
        )

    def test_backup_set_excluded_files_remove_produces_expected_pathset_value(
        self, org_device_defaults_with_multiple_values
    ):
        org_settings = OrgSettings(
            org_device_defaults_with_multiple_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        expected_path_list = [
            {"@include": TEST_HOME_DIR, "@und": "false"},
        ]
        org_settings.device_defaults.backup_sets[0].excluded_files.remove(
            TEST_PHOTOS_DIR
        )
        actual_path_list = org_settings.device_defaults["settings"][
            "serviceBackupConfig"
        ]["backupConfig"]["backupSets"]["backupSet"][0]["backupPaths"]["pathset"][
            "paths"
        ][
            "path"
        ]
        for path in expected_path_list:
            assert path in actual_path_list
        assert "excluded_files" in org_settings.device_defaults.changes
        assert (
            "-> {}".format([]) in org_settings.device_defaults.changes["excluded_files"]
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
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        org_settings.device_defaults.backup_sets[0].filename_exclusions.append(
            PHOTOS_REGEX
        )
        assert org_settings["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ]["backupSet"][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX}
        ]
        assert "filename_exclusions" in org_settings.changes
        assert PHOTOS_REGEX in org_settings.changes["filename_exclusions"]

        # single starting filename exclusion
        org_settings = OrgSettings(
            org_device_defaults_with_single_values, TEST_T_SETTINGS_DICT
        )
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        org_settings.device_defaults.backup_sets[0].filename_exclusions.append(
            PICTURES_REGEX
        )
        assert org_settings["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ]["backupSet"][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
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
        org_settings.device_defaults.backup_sets[0].pop("@locked")
        org_settings.device_defaults.backup_sets[0].filename_exclusions.append(
            NEW_REGEX
        )
        assert org_settings["deviceDefaults"]["serviceBackupConfig"]["backupConfig"][
            "backupSets"
        ]["backupSet"][0]["backupPaths"]["excludeUser"]["patternList"]["pattern"] == [
            {"@regex": PHOTOS_REGEX},
            {"@regex": PICTURES_REGEX},
            {"@regex": NEW_REGEX},
        ]
        assert "filename_exclusions" in org_settings.changes
        assert PHOTOS_REGEX in org_settings.changes["filename_exclusions"]
        assert PICTURES_REGEX in org_settings.changes["filename_exclusions"]
        assert NEW_REGEX in org_settings.changes["filename_exclusions"]
