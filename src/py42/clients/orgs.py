import json

from py42 import settings
from py42._internal.compat import ChainMap
from py42.clients import BaseClient
from py42.clients.util import get_all_pages
from py42.exceptions import Py42Error
from py42.settings import debug
from py42.util import bool_required
from py42.util import bool_to_str
from py42.util import str_to_bool


class OrgSettingsManager(object):
    def __init__(self, org_client, org_id):
        org_response = org_client.get_by_id(org_id, incSettings=True)
        org_settings_response = org_client.get_settings_by_id(org_id)

        org_dict = org_response.data
        settings_dict = org_dict.pop("settings")

        self._org = ChainMap({}, org_dict)
        self._settings = ChainMap({}, settings_dict)
        self._t_settings = ChainMap({}, org_settings_response.data)
        self._org_client = org_client
        self.errored = None
        self.org_response = None
        self.org_settings_response = None

    @property
    def changes(self):
        changes_dict = {}
        changes_dict["settings"] = self._diff_chainmap(self._org) or {}
        changes_dict["settings"].update(self._diff_chainmap(self._settings))
        t_settings_diff = list(self._diff_chainmap(self._t_settings).values())
        changes_dict["t_settings"] = t_settings_diff or None
        return changes_dict

    @property
    def org_id(self):
        return self._org["orgId"]

    @property
    def org_name(self):
        return self._org["orgName"]

    @org_name.setter
    def org_name(self, name):
        self._org["orgName"] = name

    @property
    def external_reference(self):
        return self._org["orgExtRef"]

    @external_reference.setter
    def external_reference(self, value):
        self._org["orgExtRef"] = value

    @property
    def notes(self):
        return self._org["notes"]

    @notes.setter
    def notes(self, value):
        self._org["notes"] = value

    @property
    def archive_hold_days(self):
        return self._settings["archiveHoldDays"]

    @archive_hold_days.setter
    def archive_hold_days(self, value):
        self._settings["archiveHoldDays"] = value
        self._settings["isUsingQuotaDefaults"] = False

    @property
    def max_user_subscriptions(self):
        return self._settings["maxSeats"]

    @max_user_subscriptions.setter
    def max_user_subscriptions(self, value):
        self._settings["maxSeats"] = value
        self._settings["isUsingQuotaDefaults"] = False

    @property
    def endpoint_monitoring_enabled(self):
        value = self._t_settings["org-securityTools-enable"]["value"]
        return str_to_bool(value)

    @endpoint_monitoring_enabled.setter
    @bool_required
    def endpoint_monitoring_enabled(self, value):
        self._t_settings["org-securityTools-enable"] = {
            "key": "org-securityTools-enable",
            "value": bool_to_str(value),
            "locked": False,
        }
        self._t_settings["device_advancedExfiltrationDetection_enabled"] = {
            "key": "device_advancedExfiltrationDetection_enabled",
            "value": bool_to_str(value),
            "locked": False,
        }
        if not value:  # disable everything but FMC, like the UI does
            self.endpoint_monitoring_removable_media_enabled = False
            self.endpoint_monitoring_browser_and_applications_enabled = False
            self.endpoint_monitoring_cloud_sync_enabled = False

    @property
    def endpoint_monitoring_removable_media_enabled(self):
        value = self._t_settings["org-securityTools-device-detection-enable"]["value"]
        return str_to_bool(value)

    @endpoint_monitoring_removable_media_enabled.setter
    @bool_required
    def endpoint_monitoring_removable_media_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = True
        self._t_settings["org-securityTools-device-detection-enable"] = {
            "key": "org-securityTools-device-detection-enable",
            "value": bool_to_str(value),
            "locked": False,
        }

    @property
    def endpoint_monitoring_cloud_sync_enabled(self):
        value = self._t_settings["org-securityTools-cloud-detection-enable"]["value"]
        return str_to_bool(value)

    @endpoint_monitoring_cloud_sync_enabled.setter
    @bool_required
    def endpoint_monitoring_cloud_sync_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = True
        self._t_settings["org-securityTools-cloud-detection-enable"] = {
            "key": "org-securityTools-cloud-detection-enable",
            "value": bool_to_str(value),
            "locked": False,
        }

    @property
    def endpoint_monitoring_browser_and_applications_enabled(self):
        value = self._t_settings["org-securityTools-open-file-detection-enable"][
            "value"
        ]
        return str_to_bool(value)

    @endpoint_monitoring_browser_and_applications_enabled.setter
    @bool_required
    def endpoint_monitoring_browser_and_applications_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = True
        self._t_settings["org-securityTools-open-file-detection-enable"] = {
            "key": "org-securityTools-open-file-detection-enable",
            "value": bool_to_str(value),
            "locked": False,
        }

    @property
    def endpoint_monitoring_file_metadata_enabled(self):
        value = self._t_settings["device_fileForensics_enabled"]["value"]
        return str_to_bool(value)

    @endpoint_monitoring_file_metadata_enabled.setter
    @bool_required
    def endpoint_monitoring_file_metadata_enabled(self, value):
        if value:
            self.endpoint_monitoring_enabled = True
        self._t_settings["device_fileForensics_enabled"] = {
            "key": "device_fileForensics_enabled",
            "value": bool_to_str(value),
            "locked": False,
        }

    def update(self):
        msg = "Updating org_id={}, org_name={}, with changes: {}".format(
            self.org_id, self._org.maps[1]["orgName"], self.changes
        )
        debug.logger.debug(msg)
        if self.changes["settings"]:
            self._update_settings()
        if self.changes["t_settings"]:
            self._update_org_settings()

        return "Success" if not self.errored else "Error(s) occurred."

    def _diff_chainmap(self, cm):
        updates, orig = cm.maps
        diff = {}
        for key, value in updates.items():
            if value != orig[key]:
                diff[key] = value
        return diff

    def _prepare_settings_payload(self):
        org_updates, org_original = self._org.maps
        settings_updates, settings_orig = self._settings.maps
        payload = org_original.copy()
        payload.update(org_updates)
        payload["settings"] = settings_orig.copy()
        payload["settings"].update(settings_updates)
        return payload

    def _update_settings(self):
        settings_payload = self._prepare_settings_payload()
        try:
            self.org_response = self._org_client.put_to_org_endpoint(
                self.org_id, data=settings_payload
            )
        except Py42Error as e:
            self.errored = True
            self.org_response = e

    def _update_org_settings(self):
        packet_list = list(self._t_settings.maps[0].values())
        org_settings_payload = {"packets": packet_list}
        try:
            self.org_settings_response = self._org_client.put_to_org_setting_endpoint(
                self.org_id, data=org_settings_payload
            )
        except Py42Error as e:
            self.errored = True
            self.org_settings_response = e


class OrgClient(BaseClient):
    """A client for interacting with Code42 organization APIs.

    Use the OrgClient to create and retrieve organizations. You can also use it to block and
    deactivate organizations.
    """

    def create_org(self, org_name, org_ext_ref=None, notes=None, parent_org_uid=None):
        """Creates a new organization.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-post>`__

        Args:
            org_name (str): The name of the new organization.
            org_ext_ref (str, optional): External reference information,
                such as a serial number, asset tag, employee ID, or help desk issue ID. Defaults to
                None.
            notes (str, optional): Descriptive information about the organization. Defaults to None.
            parent_org_uid (int, optional): The org UID for the parent organization. Defaults to
                None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/Org/"
        data = {
            u"orgName": org_name,
            u"orgExtRef": org_ext_ref,
            u"notes": notes,
            u"parentOrgUid": parent_org_uid,
        }
        return self._session.post(uri, data=json.dumps(data))

    def get_by_id(self, org_id, **kwargs):
        """Gets the organization with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = u"/api/Org/{}".format(org_id)
        return self._session.get(uri, params=kwargs)

    def get_by_uid(self, org_uid, **kwargs):
        """Gets the organization with the given UID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            org_uid (str): A UID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = u"/api/Org/{}".format(org_uid)
        params = dict(idType=u"orgUid", **kwargs)
        return self._session.get(uri, params=params)

    def get_settings_by_id(self, org_id, **kwargs):
        uri = u"/api/OrgSetting/{}".format(org_id)
        return self._session.get(uri)

    def get_page(self, page_num, page_size=None, **kwargs):
        """Gets an individual page of organizations.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            page_num (int): The page number to request.
            page_size (int, optional): The number of organizations to return per page.
                Defaults to `py42.settings.items_per_page`.
            kwargs (dict, optional): Additional advanced-user arguments. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        page_size = page_size or settings.items_per_page
        uri = u"/api/Org"
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._session.get(uri, params=params)

    def get_all(self, **kwargs):
        """Gets all organizations.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of organizations.
        """
        return get_all_pages(self.get_page, u"orgs", **kwargs)

    def block(self, org_id):
        """Blocks the organization with the given org ID as well as its child organizations. A
        blocked organization will not allow any of its users or devices to log in. New
        registrations will be rejected and all currently logged in clients will be logged out.
        Backups continue for any devices that are still active.
        `Rest Documentation <https://console.us.code42.com/apidocviewer/#OrgBlock-put>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/OrgBlock/{}".format(org_id)
        return self._session.put(uri)

    def unblock(self, org_id):
        """Removes a block, if one exists, on an organization and its descendants with the given
        ID. All users in the organization remain blocked until they are unblocked individually.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#OrgBlock-delete>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/OrgBlock/{}".format(org_id)
        return self._session.delete(uri)

    def deactivate(self, org_id):
        """Deactivates the organization with the given ID, including all users, plans, and
        devices. Backups stop and archives move to cold storage.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#OrgDeactivation-put>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/OrgDeactivation/{}".format(org_id)
        return self._session.put(uri)

    def reactivate(self, org_id):
        """Reactivates the organization with the given ID. Backups are *not* restarted
        automatically.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#OrgDeactivation-delete>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/OrgDeactivation/{}".format(org_id)
        return self._session.delete(uri)

    def get_current(self, **kwargs):
        """Gets the organization for the currently signed-in user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization for the
            currently signed-in user.
        """
        uri = u"/api/Org/my"
        return self._session.get(uri, params=kwargs)

    def get_agent_state(self, orgId, property_name):
        """Gets the agent state of the devices in the org.
            `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v14#/agent-state/AgentState_ViewByDeviceGuid>`__

            Args:
                orgId (str): The org's identifier.
                property_name (str): The name of the property to retrieve (e.g. `fullDiskAccess`).

            Returns:
                :class:`py42.response.Py42Response`: A response containing settings information.
            """
        uri = u"/api/v14/agent-state/view-by-organization-id"
        params = {u"orgId": orgId, u"propertyName": property_name}
        return self._session.get(uri, params=params)

    def get_agent_full_disk_access_states(self, guid):
        """Gets the full disk access status for devices in an org.
            `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v14#/agent-state/AgentState_ViewByDeviceGuid>`__

            Args:
                orgId (str): The org's identifier.

            Returns:
                :class:`py42.response.Py42Response`: A response containing settings information.
            """
        return self.get_agent_state(guid, u"fullDiskAccess")

    def put_to_org_endpoint(self, org_id, data):
        uri = "/api/Org/{}".format(org_id)
        return self._session.put(uri, data=json.dumps(data))

    def put_to_org_setting_endpoint(self, org_id, data):
        uri = u"/api/OrgSetting/{}".format(org_id)
        return self._session.put(uri, data=json.dumps(data))

    def get_settings_manager(self, org_id):
        return OrgSettingsManager(self, org_id)
