from collections import UserDict

from pycpg.clients.settings import SettingProperty
from pycpg.clients.settings import TSettingProperty
from pycpg.clients.settings._converters import bool_to_str
from pycpg.clients.settings._converters import bytes_to_gb
from pycpg.clients.settings._converters import comma_separated_to_list
from pycpg.clients.settings._converters import gb_to_bytes
from pycpg.clients.settings._converters import str_to_bool
from pycpg.clients.settings._converters import to_comma_separated
from pycpg.clients.settings._converters import to_list
from pycpg.clients.settings.device_settings import DeviceSettingsDefaults


class OrgSettings(UserDict):
    """Class used to manage an Organization's settings."""

    def __init__(self, org_settings, t_settings):
        self.data = org_settings
        self._t_settings = t_settings
        self._packets = {}
        self.changes = {}
        try:
            self.device_defaults = DeviceSettingsDefaults(
                self.data["deviceDefaults"], org_settings=self
            )
        except KeyError:
            self.device_defaults = None

    @property
    def packets(self):
        """The setting packets for any modifications to be posted to the /api/v1/OrgSettings
        endpoint.
        """
        return list(self._packets.values())

    @property
    def org_id(self):
        """The identifier for the org."""
        return self.data["orgId"]

    @property
    def registration_key(self):
        """The registration key for the org."""
        return self.data["registrationKey"]

    org_name = SettingProperty("org_name", ["orgName"])
    """Name for this Org."""

    external_reference = SettingProperty("external_reference", ["orgExtRef"])
    """External reference field for this Org."""

    notes = SettingProperty("notes", ["notes"])
    """Notes field for this Org."""

    quota_settings_inherited = SettingProperty(
        "quota_settings_inherited",
        ["settings", "isUsingQuotaDefaults"],
    )
    """Determines if Org Quota settings (`maximum_user_subscriptions`, `org_backup_quota`,
    `user_backup_quota`, `archive_hold_days`) are inherited from parent organization.

    Modifying one of the Org Quota attributes automatically sets this attribute to `False`.
    """

    archive_hold_days = SettingProperty(
        "archive_hold_days",
        ["settings", "archiveHoldDays"],
        inheritance_attr="quota_settings_inherited",
    )
    """Number of days backup archives are held in cold storage after deactivation or
    destination removal from any devices in this Org.
    """

    maximum_user_subscriptions = SettingProperty(
        "maximum_user_subscriptions",
        ["settings", "maxSeats"],
        inheritance_attr="quota_settings_inherited",
    )
    """Number of users allowed to consume a license in this Org. Set to -1 for unlimited."""

    org_backup_quota = SettingProperty(
        "org_backup_quota",
        ["settings", "maxBytes"],
        get_converter=bytes_to_gb,
        set_converter=gb_to_bytes,
        inheritance_attr="quota_settings_inherited",
    )
    """Backup storage quota (in GB) for this organization. Set to -1 for unlimited."""

    user_backup_quota = SettingProperty(
        "user_backup_quota",
        ["settings", "defaultUserMaxBytes"],
        get_converter=bytes_to_gb,
        set_converter=gb_to_bytes,
        inheritance_attr="quota_settings_inherited",
    )
    """Backup storage quota (in GB) for each user in this organization. Set to -1 for
    unlimited."""

    web_restore_admin_limit = SettingProperty(
        "web_restore_admin_limit", ["settings", "webRestoreAdminLimitMb"]
    )
    """Limit (in MB) to amount of data restorable by admin users via web restore."""

    web_restore_user_limit = SettingProperty(
        "web_restore_user_limit", ["settings", "webRestoreUserLimitMb"]
    )
    """Limit (in MB) to amount of data restorable by non-admin users via web restore."""

    reporting_settings_inherited = SettingProperty(
        "reporting_settings_inherited",
        ["settings", "isUsingReportingDefaults"],
    )
    """Determines if Org Reporting settings (`backup_warning_email_days`,
    `backup_critical_email_days', `backup_alert_recipient_emails`) are inherited from
    parent organization.

    Modifying one of the Org Reporting attributes automatically sets this attribute to
    `False`.
    """

    backup_warning_email_days = SettingProperty(
        "backup_warning_email_days",
        ["settings", "warnInDays"],
        inheritance_attr="reporting_settings_inherited",
    )
    """The number of days devices in this org can go without any backup before "warning"
    alerts get sent to org admins.
    """

    backup_critical_email_days = SettingProperty(
        "backup_critical_email_days",
        ["settings", "alertInDays"],
        inheritance_attr="reporting_settings_inherited",
    )
    """The number of days devices in this org can go without any backup before "critical"
    alerts get sent to org admins.
    """

    backup_alert_recipient_emails = SettingProperty(
        "backup_alert_recipient_emails",
        ["settings", "recipients"],
        set_converter=to_list,
        inheritance_attr="reporting_settings_inherited",
    )
    """List of email addresses that organization backup alert emails get sent to (org
    admin users get these automatically).
    """

    _endpoint_monitoring_enabled = TSettingProperty(
        "endpoint_monitoring_enabled",
        "org-securityTools-enable",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    _aed_enabled = TSettingProperty(
        "aed_enabled",
        "device_advancedExfiltrationDetection_enabled",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    _removable_media_enabled = TSettingProperty(
        "removable_media_enabled",
        "org-securityTools-device-detection-enable",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    _cloud_sync_enabled = TSettingProperty(
        "cloud_sync_enabled",
        "org-securityTools-cloud-detection-enable",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    _browser_and_applications_enabled = TSettingProperty(
        "browser_and_applications_enabled",
        "org-securityTools-open-file-detection-enable",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    _file_metadata_collection_enabled = TSettingProperty(
        "file_metadata_collection_enabled",
        "device_fileForensics_enabled",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    _printer_detection_enabled = TSettingProperty(
        "printer_detection_enabled",
        "org_securityTools_printer_detection_enable",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )

  

    web_restore_enabled = TSettingProperty(
        "web_restore_enabled",
        "device_webRestore_enabled",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if web restores are enabled for devices in this org."""

    def __repr__(self):
        return f"<OrgSettings: org_id: {self.data['orgId']}, name: '{self.data['orgName']}'>"

    def __str__(self):
        return str(self.data)
