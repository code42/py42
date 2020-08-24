import json
from collections import namedtuple

from py42 import settings
from py42.clients import BaseClient
from py42.clients._settings_managers import OrgSettingsManager
from py42.clients.util import get_all_pages
from py42.exceptions import Py42Error

OrgSettingsManagerResponse = namedtuple(
    "SettingsManagerResponse", ["error", "settings_response", "org_settings_response"]
)


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
        org_settings = self.get_by_id(org_id, incSettings=True, incDeviceDefaults=True)
        t_settings = self.get_settings_by_id(org_id)
        return OrgSettingsManager(org_settings.data, t_settings.data)

    def update_org_settings(self, org_settings_manager):
        error = False
        org_settings_response = settings_response = None

        if org_settings_manager.packets:
            payload = {"packets": org_settings_manager.packets}
            try:
                org_settings_response = self.put_to_org_setting_endpoint(
                    org_settings_manager.org_id, data=payload
                )
            except Py42Error as ex:
                error = True
                org_settings_response = ex

        if org_settings_manager.changes:
            try:
                settings_response = self.put_to_org_endpoint(
                    org_settings_manager.org_id, data=org_settings_manager.data
                )
            except Py42Error as ex:
                error = True
                settings_response = ex
        return OrgSettingsManagerResponse(
            error=error,
            settings_response=settings_response,
            org_settings_response=org_settings_response,
        )
