from py42._compat import UserDict
from py42.clients.settings import SettingProperty
from py42.clients.settings import TSettingProperty
from py42.clients.settings.converters import to_list
from py42.clients.settings.device_settings import DeviceSettingsDefaults


class OrgSettings(UserDict, object):
    """Helper class for managing Organization settings."""

    def __init__(self, org_settings, t_settings):
        self.data = org_settings
        self._t_settings = t_settings
        self._packets = {}
        self.changes = {}
        self.device_defaults = DeviceSettingsDefaults(
            self.data["deviceDefaults"], org_settings=self,
        )

    @property
    def packets(self):
        return list(self._packets.values())

    @property
    def org_id(self):
        return self.data["orgId"]

    @property
    def registration_key(self):
        return self.data["registrationKey"]

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
        "user_backup_quota_bytes", ["settings", "defaultUserMaxBytes"]
    )
    web_restore_admin_limit_mb = SettingProperty(
        "web_restore_admin_limit_mb", ["settings", "webRestoreAdminLimitMb"]
    )
    web_restore_user_limit_mb = SettingProperty(
        "web_restore_user_limit_mb", ["settings", "webRestoreUserLimitMb"]
    )
    backup_warning_email_days = SettingProperty(
        "backup_warning_email_days", ["settings", "warnInDays"]
    )
    backup_critical_email_days = SettingProperty(
        "backup_critical_email_days", ["settings", "alertInDays"]
    )
    backup_alert_recipient_emails = SettingProperty(
        "backup_alert_recipient_emails",
        ["settings", "recipients"],
        set_converter=to_list,
    )

    _endpoint_monitoring_enabled = TSettingProperty(
        "endpoint_monitoring_enabled", "org-securityTools-enable", enforce_bool=True
    )
    _aed_enabled = TSettingProperty(
        "aed_enabled", "device_advancedExfiltrationDetection_enabled", enforce_bool=True
    )
    _removable_media_enabled = TSettingProperty(
        "removable_media_enabled",
        "org-securityTools-device-detection-enable",
        enforce_bool=True,
    )
    _cloud_sync_enabled = TSettingProperty(
        "cloud_sync_enabled",
        "org-securityTools-cloud-detection-enable",
        enforce_bool=True,
    )
    _browser_and_applications_enabled = TSettingProperty(
        "browser_and_applications_enabled",
        "org-securityTools-open-file-detection-enable",
        enforce_bool=True,
    )
    _file_metadata_collection_enabled = TSettingProperty(
        "file_forensics_enabled", "device_fileForensics_enabled", enforce_bool=True
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
