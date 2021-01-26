from py42 import settings
from py42._compat import quote
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42UserAlreadyExistsError
from py42.services import BaseService
from py42.services import handle_active_legal_hold_error
from py42.services.util import get_all_pages


class UserService(BaseService):
    """A service for interacting with Code42 user APIs. Use the UserService to create and retrieve
    users. You can also use it to block and deactivate users.
    """

    def create_user(
        self,
        org_uid,
        username,
        email,
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
            email (str): The email for the new user.
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

        try:
            return self._connection.post(uri, json=data)
        except Py42InternalServerError as err:
            if u"USER_DUPLICATE" in err.response.text:
                raise Py42UserAlreadyExistsError(err)

    def get_by_id(self, user_id, **kwargs):
        """Gets the user with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User/{}".format(user_id)
        return self._connection.get(uri, params=kwargs)

    def get_by_uid(self, user_uid, **kwargs):
        """Gets the user with the given UID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            user_uid (str): A UID for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User/{}".format(user_uid)
        params = dict(idType=u"uid", **kwargs)
        return self._connection.get(uri, params=params)

    def get_by_username(self, username, **kwargs):
        """Gets the user with the given username.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            username (str or unicode): A username for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User"
        params = dict(username=username, **kwargs)
        return self._connection.get(uri, params=params)

    def get_current(self, **kwargs):
        """Gets the currently signed in user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = u"/api/User/my"
        return self._connection.get(uri, params=kwargs)

    def get_page(
        self,
        page_num,
        active=None,
        email=None,
        org_uid=None,
        role_id=None,
        page_size=None,
        q=None,
        **kwargs
    ):
        """Gets an individual page of users.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#User-get>`__

        Args:
            page_num (int): The page number to request.
            active (bool, optional): True gets active users only,
                and false gets deactivated users only. Defaults to None.
            email (str, optional): Limits users to only those with this email. Defaults to None.
            org_uid (str, optional): Limits users to only those in the organization with this org
                UID. Defaults to None.
            role_id (int, optional): Limits users to only those with a given role ID. Defaults to
                None.
            page_size (int, optional): The number of items on the page. Defaults to `py42.settings.items_per_page`.
            q (str, optional): A generic query filter that searches across name, username, and
                email. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = u"/api/User"
        page_size = page_size or settings.items_per_page
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

        return self._connection.get(uri, params=params)

    def get_all(
        self, active=None, email=None, org_uid=None, role_id=None, q=None, **kwargs
    ):
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
            self.get_page,
            u"users",
            active=active,
            email=email,
            org_uid=org_uid,
            role_id=role_id,
            q=q,
            **kwargs
        )

    def get_scim_data_by_uid(self, user_uid):
        """Returns SCIM data such as division, department, and title for a given user.
        `REST Documentation <https://console.us.code42.com/swagger/?urls.primaryName=v7#/scim-user-data>`__

        Args:
            user_uid (str): A Code42 user uid.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v7/scim-user-data/collated-view"
        params = dict(userId=user_uid)
        return self._connection.get(uri, params=params)

    def block(self, user_id):
        """Blocks the user with the given ID. A blocked user is not allowed to log in or restore
        files. Backups will continue if the user is still active.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserBlock-put>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserBlock/{}".format(user_id)
        return self._connection.put(uri)

    def unblock(self, user_id):
        """Removes a block, if one exists, on the user with the given user ID. Unblocked users are
        allowed to log in and restore.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserBlock-delete>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserBlock/{}".format(user_id)
        return self._connection.delete(uri)

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
        uri = u"/api/UserDeactivation/{}".format(user_id)
        data = {u"blockUser": block_user}
        try:
            return self._connection.put(uri, json=data)
        except Py42BadRequestError as ex:
            handle_active_legal_hold_error(ex, u"user", user_id)
            raise

    def reactivate(self, user_id, unblock_user=None):
        """Reactivates the user with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserDeactivation-delete>`__

        Args:
            user_id (int): An ID for a user.
            unblock_user (bool, optional): Whether or not to unblock the user. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserDeactivation/{}".format(user_id)
        params = {u"unblockUser": unblock_user}
        return self._connection.delete(uri, params=params)

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
        return self._connection.post(uri, json=data)

    def get_available_roles(self):
        """Report the list of roles that are available for the authenticated user to
        assign to other users.
        `V4 REST Documentation <https://console.us.code42.com/swagger/#/role/Role_View>`__

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v4/role/view"
        return self._connection.get(uri)

    def get_roles(self, user_id):
        """Return the list of roles that are currently assigned to the given user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserRole-get>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserRole/{}".format(user_id)
        return self._connection.get(uri)

    def add_role(self, user_id, role_name):
        """Adds a role to a user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#UserRole-post>`__

        Args:
            user_id (int): An ID for a user.
            role_name (str): The name of the role to assign to the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/UserRole"
        data = {u"userId": user_id, u"roleName": role_name}
        return self._connection.post(uri, json=data)

    def remove_role(self, user_id, role_name):
        """Removes a role from a user.
        REST Documentation <https://console.us.code42.com/apidocviewer/#UserRole-delete>`__

        Args:
            user_id (int): An ID for a user.
            role_name (str): The name of the role to unassign from the user.

        Returns:
            :class:`py42.response.Py42Response`
        """

        # use quote instead of params here so that %20 is used instead of + for spaces.
        role_name = quote(role_name)
        uri = u"/api/UserRole?userId={}&roleName={}".format(user_id, role_name)
        return self._connection.delete(uri)
