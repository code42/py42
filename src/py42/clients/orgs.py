import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


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
        uri = u"/api/Org/{0}".format(org_id)
        return self._session.get(uri, params=kwargs)

    def get_by_uid(self, org_uid, **kwargs):
        """Gets the organization with the given UID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            org_uid (str): A UID for an organization.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the organization.
        """
        uri = u"/api/Org/{0}".format(org_uid)
        params = dict(idType=u"orgUid", **kwargs)
        return self._session.get(uri, params=params)

    def get_by_name(self, org_name, **kwargs):
        """Gets the organization with the given name.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Org-get>`__

        Args:
            org_name (str): A name of an organization.

        Returns:
            list: A list of :class:`py42.response.Py42Response` objects each containing an
            organization that has the given name.
        """
        found_orgs = []
        response = self.get_all(**kwargs)
        for page in response:
            org_list = page[u"orgs"]
            for org in org_list:
                if org[u"orgName"] == org_name:
                    found_orgs.append(org)
        return found_orgs

    def _get_page(self, page_num=None, page_size=None, **kwargs):
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
        return get_all_pages(self._get_page, u"orgs", **kwargs)

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
        uri = u"/api/OrgBlock/{0}".format(org_id)
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
        uri = u"/api/OrgBlock/{0}".format(org_id)
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
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
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
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
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
