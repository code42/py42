from collections import namedtuple

from py42 import settings
from py42.clients.settings.org_settings import OrgSettings
from py42.exceptions import Py42Error
from py42.exceptions import Py42InternalServerError
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

    def __init__(self, connection):
        super().__init__(connection)
        self._org_id_map = {}

    @property
    def org_id_map(self):
        """Map org guids to ids."""
        if not self._org_id_map:
            self._org_id_map = {}
            page = self.get_page()
            for org in page["orgs"]:
                self._org_id_map[org["orgId"]] = org["orgGuid"]
        return self._org_id_map

    def create_org(self, org_name, org_ext_ref=None, notes=None, parent_org_uid=None):
        """Creates a new organization.

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

        # get parent org GUID from UID :)
        parent_org_guid = self._get_guid_by_id(parent_org_uid, id_key="orgUid")

        uri = "/api/v3/orgs"
        data = {
            "orgName": org_name,
            "orgExtRef": org_ext_ref,
            "notes": notes,
            "parentOrgGuid": parent_org_guid,
        }
        response = self._connection.post(uri, json=data)

        # update ID store
        self.org_id_map[response["orgId"]] = response["orgGuid"]

        return response

    def get_by_id(self, org_id, **kwargs):
        """Gets the organization with the given ID.

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = f"/api/v3/orgs/{self._get_guid_by_id(org_id)}"
        return self._connection.get(uri, params=kwargs)

    def get_by_uid(self, org_uid, **kwargs):
        """Gets the organization with the given UID.

        Args:
            org_uid (str): A UID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = f'/api/v3/orgs/{self._get_guid_by_id(org_uid, id_key="orgUid")}'
        return self._connection.get(uri, params=kwargs)

    def get_page(self, page_num=1, page_size=None, **kwargs):
        """Gets an individual page of organizations.

        Args:
            page_num (int): The page number to request.
            page_size (int, optional): The number of organizations to return per page.
                Defaults to `py42.settings.items_per_page`.
            kwargs (dict, optional): Additional advanced-user arguments. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        page_size = page_size or settings.items_per_page
        uri = "/api/v1/Org"
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._connection.get(uri, params=params)

    def get_all(self, **kwargs):
        """Gets all organizations.

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

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/orgs/{self._get_guid_by_id(org_id)}/block"
        return self._connection.post(uri)

    def unblock(self, org_id):
        """Removes a block, if one exists, on an organization and its descendants with the given
        ID. All users in the organization remain blocked until they are unblocked individually.

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/orgs/{self._get_guid_by_id(org_id)}/unblock"
        return self._connection.post(uri)

    def deactivate(self, org_id):
        """Deactivates the organization with the given ID, including all users, plans, and
        devices. Backups stop and archives move to cold storage.

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/orgs/{self._get_guid_by_id(org_id)}/deactivate"
        return self._connection.post(uri)

    def reactivate(self, org_id):
        """Reactivates the organization with the given ID. Backups are *not* restarted
        automatically.

        Args:
            org_id (int): An ID for an organization.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/orgs/{self._get_guid_by_id(org_id)}/activate"
        return self._connection.post(uri)

    def get_current(self, **kwargs):
        """Gets the organization for the currently signed-in user.

        WARNING: This method is incompatible with api client authentication.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization for the
            currently signed-in user.
        """
        uri = "/api/v1/Org/my"
        try:
            return self._connection.get(uri, params=kwargs)
        except Py42InternalServerError as err:
            raise Py42InternalServerError(
                err,
                message="Server Error. Please be aware that this method is incompatible with api client authentication.",
            )

    def get_agent_state(self, org_id, property_name):
        """Gets the agent state of the devices in the org.

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
        uri = f"/api/v1/OrgSetting/{org_id}"
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
            uri = f"/api/v1/OrgSetting/{org_id}"
            payload = {"packets": org_settings.packets}
            try:
                org_settings_response = self._connection.put(uri, json=payload)
            except Py42Error as ex:
                error = True
                org_settings_response = ex

        if org_settings.changes:
            uri = f"/api/v1/Org/{org_id}"
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

    def update_org(self, org_id, name=None, notes=None, ext_ref=None):
        """Updates an org. Only fields associated with passed parameters will be updated.


        Args:
            org_id (str): The org's identifier.
            name (str, optional): The updated name for the org.
            notes (str, optional): The updated notes for the org.
            ext_ref (str, optional): The updated external reference for the org.

        Returns:
            :class:`py42.response.Py42Response`:
        """
        uri = f"/api/v3/orgs/{self._get_guid_by_id(org_id)}"
        data = {"orgName": name, "orgExtRef": ext_ref, "notes": notes}
        self._connection.put(uri, json=data)

    def _get_guid_by_id(self, org_id, id_key="orgId"):
        # Identity crisis helper method.
        # Old orgs methods accepted IDs. New apis take GUIDs.
        # Use additional lookup to prevent breaking changes.

        if id_key != "orgId":
            guid = ""
            page = self.get_page()
            for org in page["orgs"]:
                if org[id_key] == org_id:
                    return org["orgGuid"]
            if not guid:
                raise Py42Error(f"Couldn't find an Org with ID '{org_id}'.")
        else:
            try:
                return self.org_id_map[org_id]
            except KeyError:
                raise Py42Error(f"Couldn't find an Org with ID '{org_id}'.")
