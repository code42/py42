from py42._compat import str
from py42._compat import UserDict
from py42._compat import UserList
from py42.clients.settings import check_lock
from py42.clients.settings import SettingProperty
from py42.clients.settings import show_change
from py42.clients.settings._converters import bool_to_str
from py42.clients.settings._converters import days_to_minutes
from py42.clients.settings._converters import minutes_to_days
from py42.clients.settings._converters import str_to_bool
from py42.exceptions import Py42Error

invalid_destination_error = Py42Error(
    u"Invalid destination guid or destination not offered to device's Org."
)
destination_not_added_error = Py42Error(
    u"Destination is not added to device, unable to lock."
)


class DeviceSettingsDefaults(UserDict, object):
    """Class used for managing an Organization's Device Default settings. Also acts as a
    base class for `DeviceSettings` to manage individual device settings."""

    def __init__(self, device_dict, org_settings):
        self.data = device_dict
        self._org_settings = org_settings
        self.changes = org_settings.changes
        self._destinations = org_settings.data[u"settings"][u"destinations"]
        self.data[u"settings"] = {
            u"serviceBackupConfig": self.data[u"serviceBackupConfig"]
        }
        bs = self.data[u"serviceBackupConfig"][u"backupConfig"][u"backupSets"]
        self.backup_sets = self._extract_backup_sets(bs)

    def _extract_backup_sets(self, backup_sets):
        if isinstance(backup_sets, dict):  # number of sets are locked
            backup_sets = backup_sets["backupSet"]
            if isinstance(backup_sets, dict):  # there's only one set configured
                return [BackupSet(self, backup_sets)]
            elif isinstance(backup_sets, list):
                return [
                    BackupSet(self, bs)
                    for bs in backup_sets
                    if not _backup_set_is_legal_hold(bs)
                ]
            else:
                raise Py42Error("Unable to extract backup sets: {}".format(backup_sets))
        else:
            return [
                BackupSet(self, bs)
                for bs in backup_sets
                if not _backup_set_is_legal_hold(bs)
            ]

    @property
    def available_destinations(self):
        """Returns a dict of destinations available to be used by devices. Dict keys are
        destination guids and values are destination names.
        """
        return {d[u"guid"]: d[u"destinationName"] for d in self._destinations}

    warning_email_enabled = SettingProperty(
        name=u"warning_email_enabled",
        location=[u"settings", u"serviceBackupConfig", u"warningEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if backup "warning" threshold email alerts are configured for this device."""

    critical_email_enabled = SettingProperty(
        name=u"critical_email_enabled",
        location=[u"settings", u"serviceBackupConfig", u"severeEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if backup "critical" threshold email alerts are configured for this device."""

    warning_alert_days = SettingProperty(
        name=u"warning_alert_days",
        location=[u"settings", u"serviceBackupConfig", u"minutesUntilWarning"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    """The number of days a device can go without any backup activity before
    "warning" alert threshold is passed.
    """

    critical_alert_days = SettingProperty(
        name=u"critical_alert_days",
        location=[u"settings", u"serviceBackupConfig", u"minutesUntilSevere"],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    """The number of days a device can go without any backup activity before "warning"
    alert threshold is passed.
    """

    backup_status_email_enabled = SettingProperty(
        name=u"backup_status_email_enabled",
        location=[u"settings", u"serviceBackupConfig", u"backupStatusEmailEnabled"],
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if the regularly scheduled backup status email is enabled."""

    backup_status_email_frequency_days = SettingProperty(
        name=u"backup_status_email_frequency_days",
        location=[
            u"settings",
            u"serviceBackupConfig",
            u"backupStatusEmailFreqInMinutes",
        ],
        get_converter=minutes_to_days,
        set_converter=days_to_minutes,
    )
    """Determines the frequency of the regularly scheduled backup status email."""

    def __repr__(self):
        return u"<DeviceSettingsDefaults: org_id: {}>".format(self._org_settings.org_id)


class DeviceSettings(DeviceSettingsDefaults):
    """Class used to manage an individual device's settings."""

    def __init__(self, device_dict):
        self.changes = {}
        self.data = device_dict
        self._destinations = device_dict[u"availableDestinations"]
        bs = self.data[u"settings"][u"serviceBackupConfig"][u"backupConfig"][
            u"backupSets"
        ]
        self.backup_sets = self._extract_backup_sets(bs)
        """List of :class:`BackupSet` objects used to manage this device's backup set configurations."""

    @property
    def computer_id(self):
        """Identifier of this device. Read-only."""
        return self.data[u"computerId"]

    @property
    def device_id(self):
        """Identifier of this device (alias of `.computer_id`). Read only."""
        return self.computer_id

    @property
    def guid(self):
        """Globally unique identifier of this device. Read-only."""
        return self.data[u"guid"]

    @property
    def org_id(self):
        """Identifier of the organization this device belongs to. Read-only."""
        return self.data[u"orgId"]

    @property
    def user_id(self):
        """Identifier of the user this device belongs to. Read-only."""
        return self.data[u"userId"]

    @property
    def version(self):
        """Latest reported Code42 client version number for this device. Read-only."""
        return self.data[u"version"]

    @property
    def java_memory_heap_max(self):
        """The maximum memory the client will use on its system"""
        return self.data[u"settings"][u"javaMemoryHeapMax"]

    name = SettingProperty(name=u"name", location=[u"name"])
    """Name for this device."""

    external_reference = SettingProperty(
        name=u"external_reference", location=[u"computerExtRef"]
    )
    """External reference field for this device."""

    notes = SettingProperty(name=u"notes", location=[u"notes"])
    """Notes field for this device."""

    def __repr__(self):
        return u"<DeviceSettings: guid: {}, name: {}>".format(
            self.data[u"guid"], self.data[u"name"]
        )


class BackupSet(UserDict, object):
    """Helper class for managing device backup sets and Org device default backup sets."""

    def __init__(self, settings_manager, backup_set_dict):
        self._manager = settings_manager
        self._changes = settings_manager.changes
        self.data = backup_set_dict
        includes, excludes = self._extract_file_selection_lists()
        regex_excludes = self._extract_regex_exclusions()
        self._included_files = TrackedFileSelectionList(
            self, u"included_files", includes, self._changes
        )
        self._excluded_files = TrackedFileSelectionList(
            self, u"excluded_files", excludes, self._changes
        )
        self._filename_exclusions = TrackedFileSelectionList(
            self, u"filename_exclusions", regex_excludes, self._changes
        )
        self._orig_destinations = self.destinations

    def _extract_file_selection_lists(self):
        """Converts the file selection portion of the settings dict ("pathset") into two
        lists of just paths, `included` and `excluded`.

        The "pathset" object is a different shape depending on how many paths it
        contains and whether its locked or not:
            No paths:           `[{"@cleared": "true", "@os": "Linux"}]`
            No paths locked:    `{'@locked': 'true', 'paths': {'@cleared': 'true', '@os': 'Linux'}}`
            One path:           `[{"path": {"@include": "C:/"}, "@os": "Linux"}]`
            One path locked:    `{'@locked': 'true', 'paths': {'@os': 'Linux', 'path': {'@include': 'C:/'}}}`
            One+ paths:         `[{"path": [{"@include": "C:/Users/"},{"@exclude": "C:/Users/Admin/"},],"@os": "Linux"}]`
            One+ paths locked:  `{'@locked': 'true', 'paths': {'@os': 'Linux', 'path': [{'@include': 'C:/Users/'}, {'@exclude': 'C:/Users/Admin/'}]}}`
        """
        pathset = self.data[u"backupPaths"][u"pathset"]
        if isinstance(pathset, dict):  # pathset is locked
            path_list = pathset[u"paths"].get(u"path")
        else:
            path_list = pathset[0].get(u"path")

        # no paths selected
        if path_list is None:
            return [], []

        # one path selected
        if isinstance(path_list, dict):
            path_list = [path_list]

        includes = [p[u"@include"] for p in path_list if u"@include" in p]
        excludes = [p[u"@exclude"] for p in path_list if u"@exclude" in p]
        return includes, excludes

    def _extract_regex_exclusions(self):
        """Converts the filename exclusion portion ("excludeUser") of the settings dict
        into a simple list of regex patterns.

        The "excludeUser" object is a different shape based on the number of exclusion
        patterns present and whether the setting is locked or not:
            No exclusions:          `[{"windows": [], "linux": [], "macintosh": []}]`
            No exclusions locked:   `{'@locked': 'true', 'patternList': {'windows': [], 'macintosh': [], 'linux': []}}`
            One exclusion:          `[{"windows": [], "pattern": {"@regex": ".*"}, "linux": [], "macintosh": []}]`
            One exclusion locked:   `{'@locked': 'true', 'patternList': {'pattern': {'@regex': '.*'}, 'windows': [], 'macintosh': [], 'linux': []}}`
            One+ exclusions:        `[{"windows": [], "pattern": [{"@regex": ".*1"}, {"@regex": ".*2"}],"linux": [],"macintosh": []}]
            One+ exclusion locked:  `{'@locked': 'true', 'patternList': {'pattern': [{'@regex': '.*1'}, {'@regex': '.*2'}], 'windows': [], 'macintosh': [], 'linux': []}}`
        """
        exclude_user = self.data[u"backupPaths"][u"excludeUser"]
        if isinstance(exclude_user, dict):  # exclusions are locked
            pattern_list = exclude_user[u"patternList"].get(u"pattern")
        else:
            pattern_list = exclude_user[0].get(u"pattern")
        if not pattern_list:
            return []
        if isinstance(pattern_list, dict):
            pattern_list = [pattern_list]
        return [p[u"@regex"] for p in pattern_list]

    def _build_file_selection(self):
        """Converts the user-friendly lists of included and excluded file paths back
        into a "pathset" object the api expects. Called whenever one of the file selection
        property lists (`.included_files`, `.excluded_files`) is modified.
        """
        paths = {u"@os": u"Linux", u"path": []}
        if not self._included_files:  # ignore excluded values if nothing is included
            paths[u"@cleared"] = u"true"
        else:
            path_list = []
            for path in self._included_files:
                path_list.append({u"@include": path, u"@und": u"false"})
            for path in self._excluded_files:
                path_list.append({u"@exclude": path, u"@und": u"false"})
            paths[u"path"] = path_list
            paths[u"@cleared"] = u"false"

        self.data[u"backupPaths"][u"pathset"] = {u"paths": paths}

    def _build_regex_exclusions(self):
        """Converts the user-friendly list of filename exclusions back into the
        "excludeUser" object the api expects. Called whenever the `.filename_exclusions`
        property list is modified.
        """
        patterns = []
        for regex in self._filename_exclusions:
            patterns.append({u"@regex": regex})
        user_exclude_dict = {
            u"patternList": {
                u"pattern": patterns,
                u"windows": {u"pattern": []},
                u"macintosh": {u"pattern": []},
                u"linux": {u"pattern": []},
            }
        }
        self.data[u"backupPaths"][u"excludeUser"] = user_exclude_dict

    @property
    def locked(self):
        """Indicates whether the backup set as a whole is locked. If True, individual
        settings for this backup set (except for Destination settings), cannot be modified.
        """
        return u"@locked" in self.data and str_to_bool(self.data[u"@locked"])

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
            raise AttributeError(u"included files must be a list/tuple.")

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
            raise AttributeError(u"excluded files must be a list/tuple.")

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
            raise AttributeError(u"filename exclusions must be a list/tuple.")

    @property
    def destinations(self):
        """Returns a dict of the destinations used for backup for the backup set. Dict
        keys are the destination guids, values are the destination names.
        """
        destination_dict = {}
        if u"@cleared" in self.data[u"destinations"]:
            return destination_dict
        for d in self.data[u"destinations"]:
            guid = d[u"@id"]
            dest_name = self._manager.available_destinations[guid]
            if u"@locked" in d:
                dest_name = dest_name + u" <LOCKED>"
            destination_dict[guid] = dest_name
        return destination_dict

    def add_destination(self, destination_guid):
        """Adds a destination to be used by this backup set. Raises a :class:`Py42Error` if
        the supplied destination guid is not available to the parent device/org.

        Args:
            destination_guid (str, int): The globally unique identifier of the
                destination to be added.
        """
        destination_guid = str(destination_guid)
        if destination_guid in self._manager.available_destinations:
            if destination_guid not in self.destinations:
                if not self.destinations:  # no destinations
                    self.data[u"destinations"] = [{u"@id": destination_guid}]
                else:
                    self.data[u"destinations"].append({u"@id": destination_guid})
                self._changes[u"destinations"] = show_change(
                    self._orig_destinations, self.destinations
                )
        else:
            raise invalid_destination_error

    def remove_destination(self, destination_guid):
        """Removes a destination from use by this backup set.

        Args:
            destination_guid (str, int): The globally unique identifier of the
                destination to be removed.
        """
        destination_guid = str(destination_guid)
        self._raise_if_invalid_destination(destination_guid)
        if destination_guid in self.destinations:
            for d in self.data[u"destinations"]:
                if d[u"@id"] == destination_guid:
                    self.data[u"destinations"].remove(d)
            if not self.data[u"destinations"]:  # all destinations removed
                self.data[u"destinations"] = {u"@cleared": u"true"}
            self._changes[u"destinations"] = show_change(
                self._orig_destinations, self.destinations
            )

    def lock_destination(self, destination_guid):
        """Locks an in-use destination, disallowing the device owner from removing this
        destination from their backup. Raises a :class:`Py42Error` if the supplied destination
        guid is not in use on this backup set, or not available to the parent device/org.
        """
        destination_guid = str(destination_guid)
        if destination_guid in self._manager.available_destinations:
            if destination_guid not in self.destinations:
                raise destination_not_added_error
            else:
                for d in self.data[u"destinations"]:
                    if d[u"@id"] == destination_guid:
                        d[u"@locked"] = u"true"
                self._changes[u"destinations"] = show_change(
                    self._orig_destinations, self.destinations
                )
        else:
            raise invalid_destination_error

    def unlock_destination(self, destination_guid):
        """Unlocks an in-use destination, allowing the device owner to remove this
        destination from their backup. Raises a :class:`Py42Error` if the supplied destination
        guid is not in use on this backup set, or not available to the parent device/org.
        """
        destination_guid = str(destination_guid)
        self._raise_if_invalid_destination(destination_guid)
        if destination_guid not in self.destinations:
            raise destination_not_added_error
        else:
            for d in self.data[u"destinations"]:
                if d[u"@id"] == destination_guid:
                    del d[u"@locked"]
            self._changes[u"destinations"] = show_change(
                self._orig_destinations, self.destinations
            )

    def _raise_if_invalid_destination(self, destination_guid):
        if destination_guid not in self._manager.available_destinations:
            raise invalid_destination_error

    def __repr__(self):
        if isinstance(self.data[u"name"], dict):  # name setting locked
            name = self.data[u"name"][u"#text"]
        else:
            name = self.data[u"name"]
        return u"<BackupSet: id: {}, name: '{}'>".format(self.data[u"@id"], name)

    def __str__(self):
        return str(dict(self))


class TrackedFileSelectionList(UserList, object):
    """Helper class to track modifications to file selection lists."""

    def __init__(self, backup_set, name, _list, changes_dict):
        self.backup_set = backup_set
        self.name = name
        self.orig = list(_list)
        self.data = _list
        self._changes = changes_dict

    def register_change(self):
        self.backup_set._build_file_selection()
        self.backup_set._build_regex_exclusions()
        if set(self.orig) != set(self.data):
            self._changes[self.name] = show_change(self.orig, self.data)
        elif self.name in self._changes:
            del self._changes[self.name]

    @check_lock("backup_set")
    def append(self, item):
        self.data.append(item)
        self.register_change()

    @check_lock("backup_set")
    def clear(self):
        self.data.clear()
        self.register_change()

    @check_lock("backup_set")
    def extend(self, other):
        self.data.extend(other)
        self.register_change()

    @check_lock("backup_set")
    def insert(self, i, item):
        self.data.insert(i, item)
        self.register_change()

    @check_lock("backup_set")
    def pop(self, index=-1):
        value = self.data.pop(index)
        self.register_change()
        return value

    @check_lock("backup_set")
    def remove(self, value):
        self.data.remove(value)
        self.register_change()


def _backup_set_is_legal_hold(bs):
    """A legal hold backup set has 'destinations' locked since it enforces backup to
    _all_ offered destinations for the legal hold set. This transforms the parent
    'destinations' object from a list to a dict and adds the '@locked':'true' key/value
    pair, then the actual destinations list is under a new 'destination' key.

    '@locked' also has to be present as 'destinations' also can be a dict if _no_
    destinations have been added to the set; it becomes {'@cleared': 'true'}.
    """
    return isinstance(bs["destinations"], dict) and "@locked" in bs["destinations"]
