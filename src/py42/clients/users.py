import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class UserClient(BaseClient):
    """A client for interacting with Code42 user APIs. Use the UserClient to create and retrieve
    users. You can also use it to block and deactivate users.
    """

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
        WARNING: If the provided username already exists for a user, it will be updated in the
        database instead.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-post>`__

        Args:
            org_uid (str): The org UID for the organization the new user belongs to.
            username (str): The username for the new user.
            email (str, optional): The email for the new user. Defaults to None.
            password (str, optional): The password for the new user. Defaults to None.
            first_name (str, optional): The first name for the new user. Defaults to None.
            last_name (str, optional): The last name for the new user. Defaults to None.
            notes (str, optional): Descriptive information about the user. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
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
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User/{0}".format(user_id)
        return self._session.get(uri, params=kwargs)

    def get_by_uid(self, user_uid, **kwargs):
        """Gets the user with the given UID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            user_uid (str): A UID for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User/{0}".format(user_uid)
        params = dict(idType=u"uid", **kwargs)
        return self._session.get(uri, params=params)

    def get_by_username(self, username, **kwargs):
        """Gets the user with the given username.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            username (str): A username for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User"
        params = dict(username=username, **kwargs)
        return self._session.get(uri, params=params)

    def get_current(self, **kwargs):
        """Gets the currently signed in user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
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
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            active (bool, optional): True gets active users only,
                and false gets deactivated users only. Defaults to None.
            email (str, optional): Limits users to only those with this email. Defaults to None.
            org_uid (str, optional): Limits users to only those in the organization with this org
                UID. Defaults to None.
            role_id (int, optional): Limits users to only those with a given role ID. Defaults to
                None.
            q (str, optional): A generic query filter that searches across name, username, and
                email. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of users.
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

    def get_scim_data_by_uid(self, user_uid):
        """Returns SCIM data such as division, department, and title for
        a given user.
        `REST Documentation <https://console.us.code42.com/swagger/#/scim-user-data/ScimUserData_CollatedView>

        Args:
            user_uid (str): A Code42 user uid.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v7/scim-user-data/collated-view"
        params = dict(userId=user_uid)
        return self._session.get(uri, params=params)

    def block(self, user_id):
        """Blocks the user with the given ID. A blocked user is not allowed to log in or restore
        files. Backups will continue if the user is still active.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserBlock-put>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._session.put(uri)

    def unblock(self, user_id):
        """Removes a block, if one exists, on the user with the given user ID. Unblocked users are
        allowed to log in and restore.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserBlock-delete>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._session.delete(uri)

    def deactivate(self, user_id, block_user=None):
        """Deactivates the user with the given user ID.
        Backups discontinue for a deactivated user, and their archives go to cold storage.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserDeactivation-put>`__

        Args:
            user_id (int): An ID for a user.
            block_user (bool, optional): Blocks the user upon deactivation. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        data = {u"blockUser": block_user}
        return self._session.put(uri, data=json.dumps(data))

    def reactivate(self, user_id, unblock_user=None):
        """Reactivates the user with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserDeactivation-delete>`__

        Args:
            user_id (int): An ID for a user.
            unblock_user (bool, optional): Whether or not to unblock the user. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        params = {u"unblockUser": unblock_user}
        return self._session.delete(uri, params=params)

    def change_org_assignment(self, user_id, org_id):
        """Assigns a user to a different organization.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserMoveProcess-post>`__

        Args:
            user_id (int): An ID for a user.
            org_id (int): An ID for the organization to move the user to.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserMoveProcess"
        data = {u"userId": user_id, u"parentOrgId": org_id}
        return self._session.post(uri, data=json.dumps(data))
