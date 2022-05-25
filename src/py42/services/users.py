from py42 import settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42InvalidEmailError
from py42.exceptions import Py42InvalidPasswordError
from py42.exceptions import Py42InvalidUsernameError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42OrgNotFoundError
from py42.exceptions import Py42UserAlreadyExistsError
from py42.exceptions import Py42UsernameMustBeEmailError
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

        uri = "/api/v1/User"
        data = {
            "orgUid": org_uid,
            "username": username,
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "notes": notes,
        }

        try:
            return self._connection.post(uri, json=data)
        except Py42InternalServerError as err:
            if "USER_DUPLICATE" in err.response.text:
                raise Py42UserAlreadyExistsError(err)
            raise

    def get_by_id(self, user_id, **kwargs):
        """Gets the user with the given ID.
        `Rest Documentation <https://developer.code42.com/api/#tag/User/paths/~1v1~1users~1{userId}/get>`__

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = f"/api/v1/User/{user_id}"
        return self._connection.get(uri, params=kwargs)

    def get_by_uid(self, user_uid, **kwargs):
        """Gets the user with the given UID.

        Args:
            user_uid (str): A UID for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = f"/api/v1/User/{user_uid}"
        params = dict(idType="uid", **kwargs)
        return self._connection.get(uri, params=params)

    def get_by_username(self, username, **kwargs):
        """Gets the user with the given username.

        Args:
            username (str or unicode): A username for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """

        uri = "/api/v1/User"
        params = dict(username=username, **kwargs)
        return self._connection.get(uri, params=params)

    def get_current(self, **kwargs):
        """Gets the currently signed in user.

        WARNING: This method is incompatible with api client authentication.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the user.
        """
        uri = "/api/v1/User/my"
        try:
            return self._connection.get(uri, params=kwargs)
        except Py42NotFoundError as err:
            raise Py42NotFoundError(
                err,
                message="User not found.  Please be aware that this method is incompatible with api client authentication.",
            )

    def get_page(
        self,
        page_num,
        active=None,
        email=None,
        org_uid=None,
        role_id=None,
        page_size=None,
        q=None,
        **kwargs,
    ):
        """Gets an individual page of users.

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

        uri = "/api/v1/User"
        page_size = page_size or settings.items_per_page
        params = dict(
            active=active,
            email=email,
            orgUid=org_uid,
            roleId=role_id,
            pgNum=page_num,
            pgSize=page_size,
            q=q,
            **kwargs,
        )
        try:
            return self._connection.get(uri, params=params)
        except Py42BadRequestError as err:
            if "Organization was not found" in str(err.response.text):
                raise Py42OrgNotFoundError(err, org_uid)
            raise

    def get_all(
        self, active=None, email=None, org_uid=None, role_id=None, q=None, **kwargs
    ):
        """Gets all users.

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
            "users",
            active=active,
            email=email,
            org_uid=org_uid,
            role_id=role_id,
            q=q,
            **kwargs,
        )

    def get_scim_data_by_uid(self, user_uid):
        """Returns SCIM data such as division, department, and title for a given user.

        Args:
            user_uid (str): A Code42 user uid.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v18/scim-user-data/collated-view"
        params = dict(userId=user_uid)
        return self._connection.get(uri, params=params)

    def block(self, user_id):
        """Blocks the user with the given ID. A blocked user is not allowed to log in or restore
        files. Backups will continue if the user is still active.

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/block"
        return self._connection.post(uri)

    def unblock(self, user_id):
        """Removes a block, if one exists, on the user with the given user ID. Unblocked users are
        allowed to log in and restore.

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/unblock"
        return self._connection.post(uri)

    def deactivate(self, user_id, block_user=None):
        """Deactivates the user with the given user ID.
        Backups discontinue for a deactivated user, and their archives go to cold storage.

        Args:
            user_id (int): An ID for a user.
            block_user (bool, optional): Blocks the user upon deactivation. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/deactivate"
        data = {"block": block_user}
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as ex:
            handle_active_legal_hold_error(ex, "user", user_id)
            raise

    def reactivate(self, user_id, unblock_user=None):
        """Reactivates the user with the given ID.

        Args:
            user_id (int): An ID for a user.
            unblock_user (bool, optional): Whether or not to unblock the user. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/activate"
        params = {"unblock": unblock_user}
        return self._connection.post(uri, json=params)

    def change_org_assignment(self, user_id, org_id):
        """Assigns a user to a different organization.

        Args:
            user_id (int): An ID for a user.
            org_id (int): An ID for the organization to move the user to.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/move"
        data = {"orgId": org_id}
        return self._connection.post(uri, json=data)

    def get_available_roles(self):
        """Report the list of roles that are available for the authenticated user to
        assign to other users.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v1/role"
        return self._connection.get(uri)

    def get_roles(self, user_id):
        """Return the list of roles that are currently assigned to the given user.

        Args:
            user_id (int): An ID for a user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/roles"
        return self._connection.get(uri)

    def add_role(self, user_id, role_name):
        """Adds a role to a user.

        Args:
            user_id (int): An ID for a user.
        role_name (str): The name or ID of the role to assign to the user. e.g. "Desktop User" (name) or "desktop-user" (ID)

        Returns:
            :class:`py42.response.Py42Response`
        """

        # api calls broken into helper functions to simplify testing
        role_ids = self._update_role_ids(
            role_name, self._get_role_ids(user_id), add=True
        )
        return self._update_roles(user_id, role_ids)

    def remove_role(self, user_id, role_name):
        """Removes a role from a user.

        Args:
            user_id (int): An ID for a user.
            role_name (str): The name or ID of the role to unassign from the user. e.g. "Desktop User" (name) or "desktop-user" (ID)

        Returns:
            :class:`py42.response.Py42Response`
        """

        # api calls broken into helper functions to simplify testing
        role_ids = self._update_role_ids(
            role_name, self._get_role_ids(user_id), add=False
        )
        return self._update_roles(user_id, role_ids)

    def update_user(
        self,
        user_uid,
        username=None,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
        notes=None,
        archive_size_quota_bytes=None,
    ):
        """Updates an existing user.

        Args:
            user_uid (str or int): A Code42 user UID.
            username (str, optional): The username to which the user's username will be changed. Defaults to None.
            email (str, optional): The email to which the user's email will be changed. Defaults to None.
            password (str, optional): The password to which the user's password will be changed. Defaults to None.
            first_name (str, optional): The first name to which the user's first name will be changed. Defaults to None.
            last_name (str, optional): The last name to which the user's last name will be changed. Defaults to None.
            notes (str, optional): Descriptive information about the user. Defaults to None.
            archive_size_quota_bytes (int, optional): The quota in bytes that limits the user's archive size. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = f"/api/v1/User/{user_uid}?idType=uid"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "notes": notes,
            "quotaInBytes": archive_size_quota_bytes,
        }
        try:
            return self._connection.put(uri, json=data)
        except Py42InternalServerError as err:
            response_text = str(err.response.text)
            if "USERNAME_NOT_AN_EMAIL" in response_text:
                raise Py42UsernameMustBeEmailError(err)
            elif "EMAIL_INVALID" in response_text:
                raise Py42InvalidEmailError(email, err)
            elif "NEW_PASSWORD_INVALID" in response_text:
                raise Py42InvalidPasswordError(err)
            elif "INVALID_USERNAME" in response_text:
                raise Py42InvalidUsernameError(err)
            raise

    def _get_user_uid_by_id(self, user_id):
        # Identity crisis helper method.
        # Old py42 methods accepted IDs. New apis take UIDs.
        # Use additional lookup to prevent breaking changes.
        return self.get_by_id(user_id)["userUid"]

    def _get_role_ids(self, user_id):
        return [i["roleId"] for i in self.get_roles(user_id)]

    def _update_role_ids(self, role_name, role_ids, add=True):

        for role in self.get_available_roles():
            if (role["roleName"] == role_name) or (role["roleId"] == role_name):
                if add:
                    role_ids.append(role["roleId"])
                else:
                    role_ids.remove(role["roleId"])
                break

        return role_ids

    def _update_roles(self, user_id, role_ids):
        uri = f"/api/v3/users/{self._get_user_uid_by_id(user_id)}/roles"
        data = {"roleIds": role_ids}
        return self._connection.put(uri, json=data)
