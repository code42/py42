import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class UserClient(BaseClient):
    def create_user(
        self,
        org_uid,
        username,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
        notes=None,
    ):
        """Creates a new user.
        An anomaly with this resource is that an existing username in the database will be reused
        instead of having an error thrown.

        Args:
            org_uid (str): Organization UID.
            username (str): New username.
            email (str, optional): New email.
                Required for orgs with local or RADIUS authorization if no password is provided
                (this case will create users in invite mode).
                Defaults to None.
            password (str, optional): New password.
                For orgs with local or RADIUS authorization -
                If no password is provided an email is required to create users in invite mode.
                Defaults to None.
            first_name (str, optional): New first name. Defaults to None.
            last_name (str, optional): New last name. Defaults to None.
            notes (str, optional): Descriptive information. Defaults to None.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/User"
        data = {
            u"orgUid": org_uid,
            u"username": username,
            u"email": email,
            u"password": password,
            u"firstName": first_name,
            u"lastName": last_name,
            u"notes": notes,
        }
        return self._session.post(uri, data=json.dumps(data))

    def get_by_id(self, user_id, **kwargs):
        """Gets the user with the given ID.

        Args:
            user_id (int): ID for a user.

        Returns:
            Py42Response: A response containing the user.
        """
        uri = u"/api/User/{0}".format(user_id)
        return self._session.get(uri, params=kwargs)

    def get_by_uid(self, user_uid, **kwargs):
        """Gets the user with the given UID.

        Args:
            user_uid (str): UID for a user.

        Returns:
            Py42Response: A response containing the user.
        """
        uri = u"/api/User/{0}".format(user_uid)
        params = dict(idType=u"uid", **kwargs)
        return self._session.get(uri, params=params)

    def get_by_username(self, username, **kwargs):
        """Gets the user with the given username.

        Args:
            username (str): username for a user.

        Returns:
            Py42Response: A response containing the user.
        """
        uri = u"/api/User"
        params = dict(username=username, **kwargs)
        return self._session.get(uri, params=params)

    def get_current(self, **kwargs):
        """Gets the currently signed in user.

        Returns:
            Py42Response: A response containing the user.
        """
        uri = u"/api/User/my"
        return self._session.get(uri, params=kwargs)

    def _get_page(
        self,
        active=None,
        email=None,
        org_uid=None,
        role_id=None,
        page_num=None,
        page_size=None,
        q=None,
        **kwargs
    ):
        uri = u"/api/User"
        params = dict(
            active=active,
            email=email,
            orgUid=org_uid,
            roleId=role_id,
            pgNum=page_num,
            pgSize=page_size,
            q=q,
            **kwargs
        )

        return self._session.get(uri, params=params)

    def get_all(self, active=None, email=None, org_uid=None, role_id=None, q=None, **kwargs):
        """Gets all users.

        Args:
            active (bool, optional): True means active only, false means deactivated only.
                Defaults to None.
            email (str, optional): Limits users to those with this email. Defaults to None.
            org_uid (str, optional): Limits users to an organization. Defaults to None.
            role_id (int, optional): Limits users to those with a given role ID. Defaults to None.
            q (str, optional): A generic query filter that searches across name, username, and email.
                Defaults to None.

        Returns:
            Py42Response: A response containing the users.
        """
        return get_all_pages(
            self._get_page,
            u"users",
            active=active,
            email=email,
            org_uid=org_uid,
            role_id=role_id,
            q=q,
            **kwargs
        )

    def block(self, user_id):
        """Blocks a specific user. User is not allowed to login or restore.
            Backups continue if user is still active.

        Args:
            user_id (int): An ID for a user.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._session.put(uri)

    def unblock(self, user_id):
        """Removes block on a specific user. User will be allowed to login and restore.

        Args:
            user_id (int): An ID for a user.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._session.delete(uri)

    def deactivate(self, user_id, block_user=None):
        """Deactivates a user.
            Backups are stopped and archives placed in cold storage.

        Args:
            user_id (int): An ID for a user.
            block_user (bool, optional): Blocks the user upon deactivation. Defaults to None.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        data = {u"blockUser": block_user}
        return self._session.put(uri, data=json.dumps(data))

    def reactivate(self, user_id, unblock_user=None):
        """Removes a deactivation for the user with the given ID.

        Args:
            user_id (int): An ID for a user.
            unblock_user (bool, optional):
                Whether or not to unblock the user if they are blocked upon reactivation.
                Defaults to None.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        params = {u"unblockUser": unblock_user}
        return self._session.delete(uri, params=params)

    def change_org_assignment(self, user_id, org_id):
        """Moves a user to a different organization.

        Args:
            user_id (int): An ID for a user.
            org_id (int): The ID for the org to move the user to.

        Returns:
            Py42Response: The response of the API call.
        """
        uri = u"/api/UserMoveProcess"
        data = {u"userId": user_id, u"parentOrgId": org_id}
        return self._session.post(uri, data=json.dumps(data))
