import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class OrgClient(BaseClient):
    """A client for interacting with Code42 organization APIs.

    The OrgClient has the ability to create and retrieve orgs.
    Also, it manages blocking and deactivation.
    """

    def create_org(
        self, org_name, org_ext_ref=None, notes=None, parent_org_uid=None, classification=None
    ):
        """Creates a new organization.

        Args:
            org_name (str): The name to give to the organization.
            org_ext_ref (str, optional): External reference information,
                such as a serial number, asset tag, employee ID, or help desk issue ID.
                Defaults to None.
            notes (str, optional): Descriptive information about the organization.
                Defaults to None.
            parent_org_uid (int, optional): The org UID for the parent organization.
                Defaults to None.
            classification (str, optional):
                Classification column to denote msp and reseller organizations.
                Values: BASIC, MSP, RESELLER. Defaults to None.

        Returns:
            :class:~py42.response.Py42Response
        """
        uri = u"/api/Org/"
        data = {
            u"orgName": org_name,
            u"orgExtRef": org_ext_ref,
            u"notes": notes,
            u"parentOrgUid": parent_org_uid,
            u"classification": classification,
        }
        return self._session.post(uri, data=json.dumps(data))

    def get_by_id(self, org_id, **kwargs):
        """Gets the organization with the given org ID.
        Args:
            org_id (int): An org ID for an organization.

        Returns:
            :class:~py42.response.Py42Response: A response containing the organization.
        """
        uri = u"/api/Org/{0}".format(org_id)
        return self._session.get(uri, params=kwargs)

    def get_by_uid(self, org_uid, **kwargs):
        """Gets the organization with the given UID.

        Args:
            org_uid (str): An org UID for an organization.

        Returns:
            :class:~py42.response.Py42Response: A response containing the organization.
        """
        uri = u"/api/Org/{0}".format(org_uid)
        params = dict(idType=u"orgUid", **kwargs)
        return self._session.get(uri, params=params)

    def _get_page(self, page_num=None, page_size=None, **kwargs):
        uri = u"/api/Org"
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._session.get(uri, params=params)

    def get_all(self, **kwargs):
        """Gets all organizations.

        Returns:
            generator: An object that iterates over :class:~py42.response.Py42Response objects
                that each contain a page of organizations.
        """
        return get_all_pages(self._get_page, u"orgs", **kwargs)

    def block(self, org_id):
        """Blocks the organization and child organizations with the given org ID.
        A blocked org will not allow any of its users or computers to log in,
        new registrations will be rejected and all currently logged in clients will be logged out.
        Backups continue for active devices.

        Args:
            org_id (int): ID for an organization.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return self._session.put(uri)

    def unblock(self, org_id):
        """Removes block on an org and descendants. Users need to be individually unblocked.

        Args:
            org_id (int): ID for an organization.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return self._session.delete(uri)

    def deactivate(self, org_id):
        """Deactivates the organization with the given ID.
        All users, plans, and computers are deactivated,
        which means backups are stopped and archives placed in cold storage.

        Args:
            org_id (int): ID for an organization.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return self._session.put(uri)

    def reactivate(self, org_id):
        """Removes a deactivation from the org specified in the URL.
        Backups are *not* restarted automatically.

        Args:
            org_id (int): ID for an organization.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return self._session.delete(uri)

    def get_current(self, **kwargs):
        """Gets the organization for the signed-in user.

        Returns:
            Py42Response: A response containing the organization for the signed-in user.
        """
        uri = u"/api/Org/my"
        return self._session.get(uri, params=kwargs)
