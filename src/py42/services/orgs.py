from collections import namedtuple

from py42 import settings
from py42.clients.settings.org_settings import OrgSettings
from py42.exceptions import Py42Error
from py42.services import BaseService
from py42.services.util import get_all_pages

OrgSettingsResponse = namedtuple(
    "OrgSettingsResponse", ["error", "org_response", "org_settings_response"]
)


class OrgService(BaseService):
    """A service for interacting with Code42 organization APIs.

    Use the OrgService to create and retrieve organizations. You can also use it to block and
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
        uri = "/api/Org/"
        data = {
            "orgName": org_name,
            "orgExtRef": org_ext_ref,
            "notes": notes,
            "parentOrgUid": parent_org_uid,
        }
        return self._connection.post(uri, json=data)

    def get_by_id(self, org_id, **kwargs):
        """Gets the organization with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = f"/api/Org/{org_id}"
        return self._connection.get(uri, params=kwargs)

    def get_by_uid(self, org_uid, **kwargs):
        """Gets the organization with the given UID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            org_uid (str): A UID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = f"/api/Org/{org_uid}"
        params = dict(idType="orgUid", **kwargs)
        return self._connection.get(uri, params=params)

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
        uri = "/api/Org"
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._connection.get(uri, params=params)

    def get_all(self, **kwargs):
        """Gets all organizations.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of organizations.
        """
        return get_all_pages(self.get_page, "orgs", **kwargs)

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
        uri = f"/api/OrgBlock/{org_id}"
        return self._connection.put(uri)

    def unblock(self, org_id):
        """Removes a block, if one exists, on an organization and its descendants with the given
        ID. All users in the organization remain blocked until they are unblocked individually.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#OrgBlock-delete>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/OrgBlock/{org_id}"
        return self._connection.delete(uri)

    def deactivate(self, org_id):
        """Deactivates the organization with the given ID, including all users, plans, and
        devices. Backups stop and archives move to cold storage.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#OrgDeactivation-put>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/OrgDeactivation/{org_id}"
        return self._connection.put(uri)

    def reactivate(self, org_id):
        """Reactivates the organization with the given ID. Backups are *not* restarted
        automatically.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#OrgDeactivation-delete>`__

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/OrgDeactivation/{org_id}"
        return self._connection.delete(uri)

    def get_current(self, **kwargs):
        """Gets the organization for the currently signed-in user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization for the
            currently signed-in user.
        """
        uri = "/api/Org/my"
        return self._connection.get(uri, params=kwargs)

    def get_agent_state(self, org_id, property_name):
        """Gets the agent state of the devices in the org.
            `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v14#/agent-state/AgentState_ViewByDeviceGuid>`__

            Args:
                org_id (str): The org's identifier.
                property_name (str): The name of the property to retrieve (e.g. `fullDiskAccess`).

            Returns:
                :class:`py42.response.Py42Response`: A response containing settings information.
            """
        uri = "/api/v14/agent-state/view-by-organization-id"
        params = {"orgId": org_id, "propertyName": property_name}
        return self._connection.get(uri, params=params)

    def get_agent_full_disk_access_states(self, org_id):
        """Gets the full disk access status for devices in an org.
            `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v14#/agent-state/AgentState_ViewByDeviceGuid>`__

            Args:
                org_id (str): The org's identifier.

            Returns:
                :class:`py42.response.Py42Response`: A response containing settings information.
            """
        return self.get_agent_state(org_id, "fullDiskAccess")

    def get_settings(self, org_id):
        """Gets setting data for an org and returns an `OrgSettingsManager` for the target org.

        Args:
            org_id (int,str): The identifier of the org.

        Returns:
            :class:`py42.clients._settings_managers.OrgSettings`: A class to help manage org settings.
                """
        org_settings = self.get_by_id(
            org_id, incSettings=True, incDeviceDefaults=True, incInheritedOrgInfo=True
        )
        uri = f"/api/OrgSetting/{org_id}"
        t_settings = self._connection.get(uri)
        return OrgSettings(org_settings.data, t_settings.data)

    def update_settings(self, org_settings):
        """Updates an org's settings based on changes to the passed in `OrgSettings` instance.

        Args:
            org_settings (`OrgSettings`): An `OrgSettings` instance with desired modifications to settings.

        Returns:
            :class:`py42.services.orgs.OrgSettings`: A namedtuple containing the result of the setting change api calls.
        """
        org_id = org_settings.org_id
        error = False
        org_settings_response = org_response = None

        if org_settings.packets:
            uri = f"/api/OrgSetting/{org_id}"
            payload = {"packets": org_settings.packets}
            try:
                org_settings_response = self._connection.put(uri, json=payload)
            except Py42Error as ex:
                error = True
                org_settings_response = ex

        if org_settings.changes:
            uri = f"/api/Org/{org_id}"
            try:
                org_response = self._connection.put(uri, json=org_settings.data)
            except Py42Error as ex:
                error = True
                org_response = ex
        return OrgSettingsResponse(
            error=error,
            org_response=org_response,
            org_settings_response=org_settings_response,
        )
