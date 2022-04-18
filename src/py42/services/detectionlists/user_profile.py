from warnings import warn

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CloudAliasCharacterLimitExceededError
from py42.exceptions import Py42CloudAliasLimitExceededError
from py42.services import BaseService


class DetectionListUserService(BaseService):
    """Deprecated.  Use :class:`~py42.clients.watchlists.WatchlistsClient` and :class:`~py42.clients.userriskprofile.UserRiskProfileClient` instead. Administrator utility to manage High Risk employees information.

    `Support Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Detection_list_management_APIs>`__
    """

    _resource = "v2/user"

    def __init__(self, connection, user_context, user_service):
        super().__init__(connection)
        self._user_context = user_context
        self._user_service = user_service

    def _make_uri(self, action):
        return f"{self._resource}{action}"

    def get_by_id(self, user_id):
        """Deprecated. Use userriskprofile.get_by_id() instead. Get user details by user UID.

        Args:
            user_id (str or int): UID of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "This method is deprecated. Use userriskprofile.get_by_id() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
        }
        uri = self._make_uri("/getbyid")
        return self._connection.post(uri, json=data)

    def get(self, username):
        """Deprecated. Use userriskprofile.get_by_username() instead. Get user details by username.

        Args:
            username (str): Username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "This method is deprecated. Use userriskprofile.get_by_username() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "username": username,
        }
        uri = self._make_uri("/getbyusername")
        return self._connection.post(uri, json=data)

    def update_notes(self, user_id, notes):
        """Deprecated. Use userriskprofile.update() instead. Add or update notes related to the user.

        Args:
            user_id (str or int): The user_id whose notes need to be updated.
            notes (str): User profile notes.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "This method is deprecated. Use userriskprofile.update() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "notes": notes,
        }
        uri = self._make_uri("/updatenotes")
        return self._connection.post(uri, json=data)

    def add_risk_tags(self, user_id, tags):
        """Deprecated. Use watchlists instead. Add one or more tags.

        Args:
            user_id (str or int): The user_id whose tag(s) needs to be updated.
            tags (str or list of str ): A single tag or multiple tags in a list to be added.
               e.g "tag1" or ["tag1", "tag2"]

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "Risk tags are deprecated. Use watchlists instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        if not isinstance(tags, (list, tuple)):
            tags = [tags]

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": tags,
        }
        uri = self._make_uri("/addriskfactors")
        return self._connection.post(uri, json=data)

    def remove_risk_tags(self, user_id, tags):
        """Deprecated. Use watchlists instead. Remove one or more tags.Args:

        Args:
            user_id (str or int): The user_id whose tag(s) needs to be removed.
            tags (str or list of str ): A single tag or multiple tags in a list to be removed.
               e.g "tag1" or ["tag1", "tag2"].

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "Risk tags are deprecated. Use watchlists instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        if not isinstance(tags, (list, tuple)):
            tags = [tags]

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": tags,
        }
        uri = self._make_uri("/removeriskfactors")
        return self._connection.post(uri, json=data)

    def add_cloud_alias(self, user_id, alias):
        """Deprecated. Use userriskprofile.add_cloud_aliases() instead. Add a cloud alias.

        Args:
            user_id (str or int): The user_id whose alias needs to be updated.
            alias (str): An alias to be added.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "This method is deprecated. Use userriskprofile.add_cloud_aliases() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        # check if alias > 50 characters
        # this error checking is handled by the frontend of the console
        if len(alias) > 50:
            raise Py42CloudAliasCharacterLimitExceededError

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": [alias],
        }
        uri = self._make_uri("/addcloudusernames")
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as err:
            if "Cloud usernames must be less than or equal to" in err.response.text:
                raise Py42CloudAliasLimitExceededError(err)
            raise

    def remove_cloud_alias(self, user_id, alias):
        """Deprecated. Use userriskprofile.delete_cloud_aliases() instead. Remove one or more cloud alias.

        Args:
            user_id (str or int): The user_id whose alias needs to be removed.
            alias (str): An alias to be removed.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "This method is deprecated. Use userriskprofile.delete_cloud_aliases() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": [alias],
        }
        uri = self._make_uri("/removecloudusernames")
        return self._connection.post(uri, json=data)

    def refresh(self, user_id):
        """Deprecated. Refresh SCIM attributes of a user.

        Args:
            user_id (str or int): The user_id of the user whose attributes need to be refreshed.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn("This method is deprecated.", DeprecationWarning, stacklevel=2)

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
        }
        uri = self._make_uri("/refresh")
        return self._connection.post(uri, json=data)
