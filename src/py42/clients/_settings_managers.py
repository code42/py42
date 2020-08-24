from py42._internal.compat import str
from py42._internal.compat import UserList
from py42._internal.compat import UserDict
from py42.exceptions import Py42Error


def set_val(d, keys, value):
    """Helper for setting nested values from a dict based on a list of keys."""
    d = get_val(d, keys[:-1])
    d[keys[-1]] = value


def get_val(d, keys):
    """Helper for getting nested values from a dict based on a list of keys."""
    for key in keys:
        d = d[key]
    return d


def bool_to_str(value):
    if isinstance(value, bool) or value in ("true", "false"):
        return str(value).lower()
    else:
        raise ValueError("Value must be True or False")


def str_to_bool(value):
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    else:
        return value


def days_to_minutes(days):
    return str(int(float(days) * 1440))


def minutes_to_days(minutes):
    minutes = int(minutes)
    return int(minutes / 1440)


def show_change(val1, val2):
    return "{} -> {}".format(val1, val2)


def no_conversion(x):
    return x


class SettingProperty(object):
    """Descriptor class to help manage changes to nested dict values. Assumes attributes
    being managed are on a UserDict/UserList subclass.

    Args:
        name (str): name of attribute this class manages (changes will be registered with this name).
        location (list): list of keys defining the location of the value being managed in the managed class.
        get_converter (func, optional): function to convert retrieved values to preferred format.
        set_converter (func, optional): function to convert values being set to preferred format.
    """

    def __init__(
        self, name, location, get_converter=no_conversion, set_converter=no_conversion
    ):
        self.name = name
        self.location = location
        self.init_val = None
        self.get_converter = get_converter
        self.set_converter = set_converter

    def __get__(self, instance, owner):
        val = get_val(instance.data, self.location)
        return self.get_converter(val)

    def __set__(self, instance, val):
        val = self.set_converter(val)
        self._register_change(instance, val)
        set_val(instance.data, self.location, val)

    def _register_change(self, instance, new_val):
        new_val = self.get_converter(new_val)
        if self.init_val is None:
            init_val = get_val(instance.data, self.location)
            self.init_val = self.get_converter(init_val)
        if self.init_val == new_val:
            if self.name in instance.changes:
                instance.changes.pop(self.name)
        else:
            instance.changes[self.name] = show_change(self.init_val, new_val)


class TSettingProperty(object):
    """Descriptor class to help manage transforming t_setting packet values. Assumes t_setting
    dict is stored in `._t_settings` attribute on managed instances.

    Args:
        name (str): name of attribute this class manages (changes will be registered with this name).
        key (str): name of t_setting packet this class is managing.
    """

    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.init_val = None

    def __get__(self, instance, owner):
        packet = instance._t_settings[self.key]
        return str_to_bool(packet["value"])

    def __set__(self, instance, val):
        val = bool_to_str(val)
        packet = {"key": self.key, "value": val, "locked": False}
        instance._packets[self.key] = packet
        self._register_change(instance, val)

    def _register_change(self, instance, val):
        if self.init_val is None:
            self.init_val = instance._t_settings[self.key]["value"]
        if self.init_val == val:
            if self.name in instance.changes:
                instance.changes.pop(self.name)
        else:
            instance.changes[self.name] = show_change(self.init_val, val)


class TrackedFileSelectionList(UserList):
    """Helper class to track modifications to file selection lists."""

    def __init__(self, manager, name, _list, changes_dict):
        self.manager = manager
        self.name = name
        self.orig = list(_list)
        self.data = _list
        self._changes = changes_dict

    def register_change(self):
        self.manager._build_file_selection()
        self.manager._build_regex_exclusions()
        if set(self.orig) != set(self.data):
            self._changes[self.name] = show_change(self.orig, self.data)
        elif self.name in self._changes:
            del self._changes[self.name]

    def append(self, item):
        self.data.append(item)
        self.register_change()

    def clear(self):
        self.data.clear()
        self.register_change()

    def extend(self, other):
        self.data.extend(other)
        self.register_change()

    def insert(self, i, item):
        self.data.insert(i, item)
        self.register_change()

    def pop(self, index=-1):
        value = self.data.pop(index)
        self.register_change()
        return value

    def remove(self, value):
        self.data.remove(value)
        self.register_change()


class OrgSettingsManager(UserDict):
    """Helper class for managing Organization settings."""

    def __init__(self, org_settings, t_settings):
        self.data = org_settings
        self._t_settings = t_settings
        self._packets = {}
        self.changes = {}
        self.device_defaults = DeviceSettingsManager(
            self.data["deviceDefaults"], org_manager=self,
        )

    @property
    def packets(self):
        return list(self._packets.values())

    @property
    def org_id(self):
        return self.data["orgId"]

    org_name = SettingProperty("org_name", ["orgName"])
    external_reference = SettingProperty("external_reference", ["orgExtRef"])
    notes = SettingProperty("notes", ["notes"])
    archive_hold_days = SettingProperty(
        "archive_hold_days", ["settings", "archiveHoldDays"]
    )
    maximum_user_subscriptions = SettingProperty(
        "maximum_user_subscriptions", ["settings", "maxSeats"]
    )
    org_backup_quota_bytes = SettingProperty(
        "org_backup_quota_bytes", ["settings", "maxBytes"]
    )
    user_backup_quota_bytes = SettingProperty(
        "user_backup_quota_bytes", ["settings", "maxBytes"]
    )
    web_restore_admin_limit_mb = SettingProperty(
        "web_restore_admin_limit_mb", ["settings", "webRestoreAdminLimitMb"]
    )
    web_restore_user_limit_mb = SettingProperty(
        "web_restore_user_limit_mb", ["settings", "webRestoreUserLimitMb"]
    )
    _endpoint_monitoring_enabled = TSettingProperty(
        "endpoint_monitoring_enabled", "org-securityTools-enable"
    )
    _aed_enabled = TSettingProperty(
        "aed_enabled", "device_advancedExfiltrationDetection_enabled"
    )
    _removable_media_enabled = TSettingProperty(
        "removable_media_enabled", "org-securityTools-device-detection-enable"
    )
    _cloud_sync_enabled = TSettingProperty(
        "cloud_sync_enabled", "org-securityTools-cloud-detection-enable"
    )
    _browser_and_applications_enabled = TSettingProperty(
        "browser_and_applications_enabled",
        "org-securityTools-open-file-detection-enable",
    )
    _file_metadata_collection_enabled = TSettingProperty(
        "file_forensics_enabled", "device_fileForensics_enabled"
    )

    @property
    def endpoint_monitoring_enabled(self):
        return self._endpoint_monitoring_enabled

    @endpoint_monitoring_enabled.setter
    def endpoint_monitoring_enabled(self, val):
        self._endpoint_monitoring_enabled = val
        self._aed_enabled = val
        if not val:
            self._cloud_sync_enabled = val
            self._browser_and_applications_enabled = val
            self._removable_media_enabled = val

    @property
    def endpoint_monitoring_removable_media_enabled(self):
        return self._removable_media_enabled

    @endpoint_monitoring_removable_media_enabled.setter
    def endpoint_monitoring_removable_media_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._removable_media_enabled = value

    @property
    def endpoint_monitoring_cloud_sync_enabled(self):
        return self._cloud_sync_enabled

    @endpoint_monitoring_cloud_sync_enabled.setter
    def endpoint_monitoring_cloud_sync_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._cloud_sync_enabled = value

    @property
    def endpoint_monitoring_browser_and_applications_enabled(self):
        return self._browser_and_applications_enabled

    @endpoint_monitoring_browser_and_applications_enabled.setter
    def endpoint_monitoring_browser_and_applications_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._browser_and_applications_enabled = value

    @property
    def endpoint_monitoring_file_metadata_collection_enabled(self):
        return self._file_metadata_collection_enabled

    @endpoint_monitoring_file_metadata_collection_enabled.setter
    def endpoint_monitoring_file_metadata_collection_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._file_metadata_collection_enabled = value


class DeviceSettingsManager(UserDict):
    """Helper class for managing Device settings and Org Device Default settings."""

    def __init__(self, device_dict, org_manager=None):
        self.data = device_dict
        if org_manager:
            self.changes = org_manager.changes
            destinations = org_manager.data["settings"]["destinations"]
            service_config = self.data["serviceBackupConfig"]
        else:
            self.changes = {}
            destinations = device_dict["availableDestinations"]
            service_config = self.data["settings"]["serviceBackupConfig"]
        self.available_destinations = {
            d["guid"]: d["destinationName"] for d in destinations
        }
        self.backup_sets = [
            BackupSetManager(self, self.changes, backup_set)
            for backup_set in service_config["backupConfig"]["backupSets"]
        ]

    name = SettingProperty(name="name", location=["name"])
    external_reference = SettingProperty(
        name="external_reference", location=["computerExtRef"]
    )
    notes = SettingProperty(name="notes", location=["notes"])
    wan_throttle_away_KBps = SettingProperty(
        name="wan_throttle_away",
        location=["settings", "serviceBackupConfig", "highBandwidthRate"],
    )
    wan_throttle_present_KBps = SettingProperty(
        name="wan_throttle_present",
        location=["settings", "serviceBackupConfig", "lowBandwidthRate"],
    )
    lan_throttle_away_KBps = SettingProperty(
        name="lan_throttle_away",
        location=["settings", "serviceBackupConfig", "lanHighBandwidthRate"],
    )
    lan_throttle_present_KBps = SettingProperty(
        name="lan_throttle_present",
        location=["settings", "serviceBackupConfig", "lanLowBandwidthRate"],
    )
    warning_email_enabled = SettingProperty(
        name="warning_email_enabled",
        location=["settings", "serviceBackupConfig", "warningEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    critical_email_enabled = SettingProperty(
        name="critical_email_enabled",
        location=["settings", "serviceBackupConfig", "severeEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    warning_alert_days = SettingProperty(
        name="warning_alert_days",
        location=["settings", "serviceBackupConfig", "minutesUntilWarning"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    critical_alert_days = SettingProperty(
        name="critical_alert_days",
        location=["settings", "serviceBackupConfig", "minutesUntilSevere"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    backup_status_email_enabled = SettingProperty(
        name="backup_status_email_enabled",
        location=["settings", "serviceBackupConfig", "backupStatusEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    backup_status_email_frequency_days = SettingProperty(
        name="backup_status_email_frequency_days",
        location=["settings", "serviceBackupConfig", "backupStatusEmailFreqInMinutes"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )

    def __repr__(self):
        return "<DeviceSettingsManager: guid: {}, name: {}>".format(
            self.data["guid"], self.data["name"]
        )


class BackupSetManager(UserDict):
    """Helper class for managing device backup sets and Org device default backup sets."""

    def __init__(self, settings_manager, changes_dict, backup_set_dict):
        self._manager = settings_manager
        self._changes = changes_dict
        self.data = backup_set_dict
        includes, excludes = self._extract_file_selection_lists()
        regex_excludes = self._extract_regex_exclusions()
        self.included_files = TrackedFileSelectionList(
            self, "included_files", includes, self._changes
        )
        self.excluded_files = TrackedFileSelectionList(
            self, "excluded_files", excludes, self._changes
        )
        self.filename_exclusions = TrackedFileSelectionList(
            self, "filename_exclusions", regex_excludes, self._changes
        )
        self._orig_destinations = self.destinations

    @property
    def destinations(self):
        destination_dict = {}
        for d in self.data["destinations"]:
            guid = d["@id"]
            dest_name = self._manager.available_destinations[guid]
            if "@locked" in d:
                dest_name = dest_name + " <LOCKED>"
            destination_dict[guid] = dest_name
        return destination_dict

    def add_destination(self, destination_guid):
        destination_guid = str(destination_guid)
        if destination_guid in self._manager.available_destinations:
            if destination_guid not in self.destinations:
                self.data["destinations"].append({"@id": destination_guid})
                self._changes["destinations"] = show_change(
                    self._orig_destinations, self.destinations
                )
        else:
            raise Py42Error(
                "Invalid destination guid or destination not offered to device's Org."
            )

    def remove_destination(self, destination_guid):
        destination_guid = str(destination_guid)
        self._raise_if_invalid_destination(destination_guid)
        if destination_guid in self.destinations:
            for d in self.data["destinations"]:
                if d["@id"] == destination_guid:
                    self.data["destinations"].remove(d)
            self._changes["destinations"] = show_change(
                self._orig_destinations, self.destinations
            )

    def lock_destination(self, destination_guid):
        destination_guid = str(destination_guid)
        if destination_guid in self._manager.available_destinations:
            if destination_guid not in self.destinations:
                raise Py42Error("Destination is not added to device, unable to lock.")
            else:
                for d in self.data["destinations"]:
                    if d["@id"] == destination_guid:
                        d["@locked"] = "true"
                self._changes["destinations"] = show_change(
                    self._orig_destinations, self.destinations
                )
        else:
            raise Py42Error(
                "Invalid destination guid or destination not offered to device's Org."
            )

    def unlock_destination(self, destination_guid):
        destination_guid = str(destination_guid)
        self._raise_if_invalid_destination(destination_guid)
        if destination_guid not in self.destinations:
            raise Py42Error("Destination is not added to device, unable to unlock.")
        else:
            for d in self.data["destinations"]:
                if d["@id"] == destination_guid:
                    del d["@locked"]
            self._changes["destinations"] = show_change(
                self._orig_destinations, self.destinations
            )

    def _raise_if_invalid_destination(self, destination_guid):
        if destination_guid not in self._manager.available_destinations:
            raise Py42Error(
                "Invalid destination guid or destination not offered to device's Org."
            )

    def _extract_file_selection_lists(self):
        try:
            pathset = self.data["backupPaths"]["pathset"][0]["path"]
        except KeyError:  # no files selected
            return [], []
        if isinstance(pathset, dict):
            pathset = [pathset]
        includes = [p["@include"] for p in pathset if "@include" in p]
        excludes = [p["@exclude"] for p in pathset if "@exclude" in p]
        return includes, excludes

    def _build_file_selection(self):
        if not self.included_files:
            self.data["backupPaths"]["pathset"] = {
                "paths": {"@cleared": "true", "@os": "Linux", "path": []}
            }
            return
        pathset = []
        for path in self.included_files:
            pathset.append({"@include": path, "@und": "false"})
        for path in self.excluded_files:
            pathset.append({"@exclude": path, "@und": "false"})
        self.data["backupPaths"]["pathset"] = {
            "paths": {"@os": "Linux", "path": pathset, "@cleared": "false"}
        }

    def _extract_regex_exclusions(self):
        exclude_user = self.data["backupPaths"]["excludeUser"][0]
        pattern_list = exclude_user.get("pattern")
        if not pattern_list:
            return []
        if isinstance(pattern_list, dict):
            pattern_list = [pattern_list]
        return [p["@regex"] for p in pattern_list]

    def _build_regex_exclusions(self):
        patterns = []
        for regex in self.filename_exclusions:
            patterns.append({"@regex": regex})
        user_exclude_dict = {
            "patternList": {
                "pattern": patterns,
                "windows": {"pattern": []},
                "macintosh": {"pattern": []},
                "linux": {"pattern": []},
            }
        }
        self.data["backupPaths"]["excludeUser"] = user_exclude_dict

    def __repr__(self):
        return "<BackupSet: id: {}, name: '{}'>".format(
            self.data["@id"], self.data["name"]
        )

    def __str__(self):
        return str(dict(self))
