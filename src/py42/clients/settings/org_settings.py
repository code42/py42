from collections import UserDict

from py42.clients.settings import SettingProperty
from py42.clients.settings import TSettingProperty
from py42.clients.settings._converters import bool_to_str
from py42.clients.settings._converters import bytes_to_gb
from py42.clients.settings._converters import comma_separated_to_list
from py42.clients.settings._converters import gb_to_bytes
from py42.clients.settings._converters import str_to_bool
from py42.clients.settings._converters import to_comma_separated
from py42.clients.settings._converters import to_list
from py42.clients.settings.device_settings import DeviceSettingsDefaults


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

    @property
    def endpoint_monitoring_enabled(self):
        """Determines if endpoint monitoring settings are enabled for this org.

        Disabling this property also disables "removable media", "cloud sync",
        "browser and application monitoring" and "printer detection" properties.
        """
        return self._endpoint_monitoring_enabled

    @endpoint_monitoring_enabled.setter
    def endpoint_monitoring_enabled(self, val):
        self._endpoint_monitoring_enabled = val
        self._aed_enabled = val
        if not val:
            self._cloud_sync_enabled = val
            self._browser_and_applications_enabled = val
            self._removable_media_enabled = val
            self._printer_detection_enabled = val

    @property
    def endpoint_monitoring_removable_media_enabled(self):
        """Determines if removable media endpoint monitoring event capturing is enabled
        for this org.
        """
        return self._removable_media_enabled

    @endpoint_monitoring_removable_media_enabled.setter
    def endpoint_monitoring_removable_media_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._removable_media_enabled = value

    @property
    def endpoint_monitoring_cloud_sync_enabled(self):
        """Determines if cloud sync endpoint monitoring event capturing is enabled
        for this org.
        """
        return self._cloud_sync_enabled

    @endpoint_monitoring_cloud_sync_enabled.setter
    def endpoint_monitoring_cloud_sync_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._cloud_sync_enabled = value

    @property
    def endpoint_monitoring_browser_and_applications_enabled(self):
        """Determines if browser and other application activity endpoint monitoring
        event capturing is enabled for this org.
        """
        return self._browser_and_applications_enabled

    @endpoint_monitoring_browser_and_applications_enabled.setter
    def endpoint_monitoring_browser_and_applications_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._browser_and_applications_enabled = value

    @property
    def endpoint_monitoring_printer_detection_enabled(self):
        """Determines if printer endpoint monitoring event capturing is enabled for this
        org.
        """
        return self._printer_detection_enabled

    @endpoint_monitoring_printer_detection_enabled.setter
    def endpoint_monitoring_printer_detection_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._printer_detection_enabled = value

    @property
    def endpoint_monitoring_file_metadata_collection_enabled(self):
        """Determines if file metadata collection is enabled for this org."""
        return self._file_metadata_collection_enabled

    @endpoint_monitoring_file_metadata_collection_enabled.setter
    def endpoint_monitoring_file_metadata_collection_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = value
        self._file_metadata_collection_enabled = value

    endpoint_monitoring_file_metadata_scan_enabled = TSettingProperty(
        "file_metadata_scan_enabled",
        "device_fileForensics_scan_enabled",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if file metadata collection regular full scans are enabled for this
    org.
    """

    endpoint_monitoring_file_metadata_ingest_scan_enabled = TSettingProperty(
        "file_metadata_ingest_scan_enabled",
        "device_fileForensics_enqueue_scan_events_during_ingest",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if file metadata collection does an initial full scan when first
    enabled on devices.
    """

    endpoint_monitoring_background_priority_enabled = TSettingProperty(
        "background_priority_enabled",
        "device_background_priority_enabled",
        get_converter=str_to_bool,
        set_converter=bool_to_str,
    )
    """Determines if devices in this org have reduced priority in some IO bound tasks.
    If enabled, devices may see improved general device performance at the expense of
    some Code42 backup/security tasks taking longer.
    """

    endpoint_monitoring_custom_applications_win = TSettingProperty(
        "custom_monitored_applications_win",
        "device_org_winAppActivity_binaryWhitelist",
        get_converter=comma_separated_to_list,
        set_converter=to_comma_separated,
    )
    """List of additional applications the Code42 client monitors for file exfiltration
    activity.

    See `Support Documentation <https://support.code42.com/Administrator/Cloud/Configuring/Customize_applications_monitored_for_file_exfiltration>`__
    for more details.
    """

    endpoint_monitoring_custom_applications_mac = TSettingProperty(
        "custom_monitored_applications_mac",
        "device_org_macAppActivity_binaryWhitelist",
        get_converter=comma_separated_to_list,
        set_converter=to_comma_separated,
    )
    """List of additional applications the Code42 client monitors for file exfiltration
    activity.

    See `Support Documentation <https://support.code42.com/Administrator/Cloud/Configuring/Customize_applications_monitored_for_file_exfiltration>`__
    for more details.
    """

    endpoint_monitoring_file_metadata_collection_exclusions = TSettingProperty(
        "file_metadata_collection_exclusions",
        "device_fileForensics_fileExclusions_org",
    )
    """File types and file paths to exclude from file metadata collection.

    See `Support Documentation <https://support.code42.com/Administrator/Cloud/Configuring/File_Metadata_Collection_exclusions>`__
    for more details on the shape of the body this setting expects.
    """

    endpoint_monitoring_file_exfiltration_detection_exclusions = TSettingProperty(
        "file_exfiltration_detection_exclusions",
        "org_securityTools_detection_monitoring_exclusions",
    )
    """File types and file paths to exclude from file exfiltration detection.

    See `Support Documentation <https://support.code42.com/Administrator/Cloud/Configuring/Endpoint_monitoring#ExcludePaths>`__
    for more details on the shape of the body this setting expects.
    """

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
