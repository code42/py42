from py42._compat import str
from py42._compat import UserDict
from py42._compat import UserList
from py42.clients.settings import SettingProperty
from py42.clients.settings import show_change
from py42.clients.settings._converters import bool_to_str
from py42.clients.settings._converters import days_to_minutes
from py42.clients.settings._converters import minutes_to_days
from py42.clients.settings._converters import str_to_bool
from py42.exceptions import Py42Error


class DeviceSettingsDefaults(UserDict, object):
    """Class used for managing an Organization's Device Default settings. Also acts as a
    base class for `DeviceSettings` to manage individual device settings."""

    def __init__(self, device_dict, org_settings):
        self.data = device_dict
        self._org_settings = org_settings
        self.changes = org_settings.changes
        self._destinations = org_settings.data["settings"]["destinations"]
        self.data["settings"] = {
            "serviceBackupConfig": self.data["serviceBackupConfig"]
        }
        self.backup_sets = [
            BackupSet(self, self.changes, backup_set)
            for backup_set in self.data["serviceBackupConfig"]["backupConfig"][
                "backupSets"
            ]
        ]

    @property
    def available_destinations(self):
        """Returns a dict of destinations available to be used by devices. Dict keys are
        destination guids and values are destination names.
        """
        return {d["guid"]: d["destinationName"] for d in self._destinations}

    warning_email_enabled = SettingProperty(
        name="warning_email_enabled",
        location=["settings", "serviceBackupConfig", "warningEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if backup "warning" threshold email alerts are configured for this device."""

    critical_email_enabled = SettingProperty(
        name="critical_email_enabled",
        location=["settings", "serviceBackupConfig", "severeEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if backup "critical" threshold email alerts are configured for this device."""

    warning_alert_days = SettingProperty(
        name="warning_alert_days",
        location=["settings", "serviceBackupConfig", "minutesUntilWarning"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    """The number of days a device can go without any backup activity before
    "warning" alert threshold is passed.
    """

    critical_alert_days = SettingProperty(
        name="critical_alert_days",
        location=["settings", "serviceBackupConfig", "minutesUntilSevere"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    """The number of days a device can go without any backup activity before "warning"
    alert threshold is passed.
    """

    backup_status_email_enabled = SettingProperty(
        name="backup_status_email_enabled",
        location=["settings", "serviceBackupConfig", "backupStatusEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if the regularly scheduled backup status email is enabled."""

    backup_status_email_frequency_days = SettingProperty(
        name="backup_status_email_frequency_days",
        location=["settings", "serviceBackupConfig", "backupStatusEmailFreqInMinutes"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    """Determines the frequency of the regularly scheduled backup status email."""

    def __repr__(self):
        return "<DeviceSettingsDefaults: org_id: {}>".format(self._org_settings.org_id)


class DeviceSettings(DeviceSettingsDefaults):
    """Class used to manage an individual device's settings."""

    def __init__(self, device_dict):
        self.changes = {}
        self.data = device_dict
        self._destinations = device_dict["availableDestinations"]
        self.backup_sets = [
            BackupSet(self, self.changes, backup_set)
            for backup_set in self.data["settings"]["serviceBackupConfig"][
                "backupConfig"
            ]["backupSets"]
        ]
        """List of :class:`BackupSet` objects used to manage this device's backup set configurations."""

    @property
    def computer_id(self):
        """Identifier of this device. Read-only."""
        return self.data["computerId"]

    @property
    def guid(self):
        """Globally unique identifier of this device. Read-only."""
        return self.data["guid"]

    @property
    def org_id(self):
        """Identifier of the organization this device belongs to. Read-only."""
        return self.data["orgId"]

    @property
    def user_id(self):
        """Identifier of the user this device belongs to. Read-only."""
        return self.data["userId"]

    @property
    def version(self):
        """Latest reported Code42 client version number for this device. Read-only."""
        return self.data["version"]

    name = SettingProperty(name="name", location=["name"])
    """Name for this device."""

    external_reference = SettingProperty(
        name="external_reference", location=["computerExtRef"]
    )
    """External reference field for this device."""

    notes = SettingProperty(name="notes", location=["notes"])
    """Notes field for this device."""

    def __repr__(self):
        return "<DeviceSettings: guid: {}, name: {}>".format(
            self.data["guid"], self.data["name"]
        )


class BackupSet(UserDict, object):
    """Helper class for managing device backup sets and Org device default backup sets."""

    def __init__(self, settings_manager, changes_dict, backup_set_dict):
        self._manager = settings_manager
        self._changes = changes_dict
        self.data = backup_set_dict
        includes, excludes = self._extract_file_selection_lists()
        regex_excludes = self._extract_regex_exclusions()
        self._included_files = TrackedFileSelectionList(
            self, "included_files", includes, self._changes
        )
        self._excluded_files = TrackedFileSelectionList(
            self, "excluded_files", excludes, self._changes
        )
        self._filename_exclusions = TrackedFileSelectionList(
            self, "filename_exclusions", regex_excludes, self._changes
        )
        self._orig_destinations = self.destinations

    @property
    def included_files(self):
        """Returns the list of files/folders included in the backup selection. Items can
        be added/removed from this list via normal list methods, or assigning a new list
        of files to this attribute to replace the existing one.
        """
        return self._included_files

    @included_files.setter
    def included_files(self, value):
        if isinstance(value, (list, tuple)):
            self._included_files.clear()
            self._included_files.extend(value)
        else:
            raise AttributeError("included files must be a list/tuple.")

    @property
    def excluded_files(self):
        """Returns the list of files/folders excluded from the backup selection. Items can
        be added/removed from this list via normal list methods, or assigning a new list
        of files to this attribute to replace the existing one.
        """
        return self._excluded_files

    @excluded_files.setter
    def excluded_files(self, value):
        if isinstance(value, (list, tuple)):
            self._excluded_files.clear()
            self._excluded_files.extend(value)
        else:
            raise AttributeError("excluded files must be a list/tuple.")

    @property
    def filename_exclusions(self):
        """Returns the list of regex patterns used to exclude file paths from the backup
        selection. Items can be added/removed from this list via normal list methods,
        or assigning a new list of patterns to this attribute to replace the existing
        one.
        """
        return self._filename_exclusions

    @filename_exclusions.setter
    def filename_exclusions(self, value):
        if isinstance(value, (list, tuple)):
            self._filename_exclusions.clear()
            self._filename_exclusions.extend(value)
        else:
            raise AttributeError("filename exclusions must be a list/tuple.")

    @property
    def destinations(self):
        """Returns a dict of the destinations used for backup for the backup set. Dict
        keys are the destination guids, values are the destination names.
        """
        destination_dict = {}
        for d in self.data["destinations"]:
            guid = d["@id"]
            dest_name = self._manager.available_destinations[guid]
            if "@locked" in d:
                dest_name = dest_name + " <LOCKED>"
            destination_dict[guid] = dest_name
        return destination_dict

    def add_destination(self, destination_guid):
        """Adds a destination to be used by this backup set. Raises an exception if
        the supplied destination guid is not available to the parent device/org.

        Args:
            destination_guid (str, int): The globally unique identifier of the
            destination to be added.
        """
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
        """Removes a destination from use by this backup set.

        Args:
            destination_guid (str, int): The globally unique identifier of the
            destination to be removed.
        """
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
        """Locks an in-use destination, disallowing the device owner from removing this
        destination from their backup. Raises an exception if the supplied destination
        guid is not in use on this backup set, or not available to the parent device/org.
        """
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
        """Unlocks an in-use destination, allowing the device owner to remove this
        destination from their backup. Raises an exception if the supplied destination
        guid is not in use on this backup set, or not available to the parent device/org.
        """
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
        if not self._included_files:
            self.data["backupPaths"]["pathset"] = {
                "paths": {"@cleared": "true", "@os": "Linux", "path": []}
            }
            return
        pathset = []
        for path in self._included_files:
            pathset.append({"@include": path, "@und": "false"})
        for path in self._excluded_files:
            pathset.append({"@exclude": path, "@und": "false"})
        self.data["backupPaths"]["pathset"] = {
            "paths": {"@os": "Linux", "path": pathset, "@cleared": "false",}
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
        for regex in self._filename_exclusions:
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


class TrackedFileSelectionList(UserList, object):
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
