from py42.choices import Choices
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42UnableToCreateProfileError


class RiskTags(Choices):
    """Risk tags are DEPRECATED. Use :class:`~py42.clients.watchlists.WatchlistsClient` and :class:`~py42.clients.watchlists.WatchlistTypeClient` Constants instead.

    Constants available as risk tags for :meth:`~py42.clients.detectionlists.DetectionListsClient.add_user_risk_tags()`
    and :meth:`~py42.clients.detectionlists.DetectionListsClient.remove_user_risk_tags()`.

        * ``FLIGHT_RISK``
        * ``HIGH_IMPACT_EMPLOYEE``
        * ``ELEVATED_ACCESS_PRIVILEGES``
        * ``PERFORMANCE_CONCERNS``
        * ``SUSPICIOUS_SYSTEM_ACTIVITY``
        * ``POOR_SECURITY_PRACTICES``
        * ``CONTRACT_EMPLOYEE``
    """

    FLIGHT_RISK = "FLIGHT_RISK"
    HIGH_IMPACT_EMPLOYEE = "HIGH_IMPACT_EMPLOYEE"
    ELEVATED_ACCESS_PRIVILEGES = "ELEVATED_ACCESS_PRIVILEGES"
    PERFORMANCE_CONCERNS = "PERFORMANCE_CONCERNS"
    SUSPICIOUS_SYSTEM_ACTIVITY = "SUSPICIOUS_SYSTEM_ACTIVITY"
    POOR_SECURITY_PRACTICES = "POOR_SECURITY_PRACTICES"
    CONTRACT_EMPLOYEE = "CONTRACT_EMPLOYEE"


class DetectionListsClient:
    """DEPRECATED.  Use the :class:`~py42.clients.watchlists.WatchlistsClient` and :class:`~py42.clients.userriskprofile.UserRiskProfileClient` instead.

    A client to expose the detectionlists API.

    `Rest documentation <https://developer.code42.com/api/#tag/Detection-Lists>`__"""

    def __init__(
        self,
        user_profile_service,
        departing_employee_service,
        high_risk_employee_service,
        user_risk_profile_service,
        watchlist_service,
    ):
        self._user_profile_service = user_profile_service
        self._departing_employee_service = departing_employee_service
        self._high_risk_employee_service = high_risk_employee_service
        self._user_risk_profile_service = user_risk_profile_service
        self._watchlist_service = watchlist_service

    @property
    def departing_employee(self):
        return self._departing_employee_service

    @property
    def high_risk_employee(self):
        return self._high_risk_employee_service

    def create_user(self, username):
        """DEPRECATED. Used to create a detection list profile for a user, but now that
        happens automatically. Thus, this method instead returns the response from
        an API call that gets the user's profile.

        Args:
            username (str): The Code42 username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        try:
            return self._user_profile_service.get(username)  # TODO
        except Py42BadRequestError as err:
            if "Could not find user" in str(err):
                raise Py42UnableToCreateProfileError(err, username)
            raise

    def get_user(self, username):
        """DEPRECATED. TODO

        Get user details by username.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_GetByUsername>`__

        Args:
            username (str): The Code42 username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.get(username)  # TODO

    def get_user_by_id(self, user_id):
        """DEPRECATED. TODO
        Get user details by user_id.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_GetByUserId>`__

        Args:
            user_id (str or int): The Code42 userId of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.get(user_id)

    def update_user_notes(self, user_id, notes):
        """DEPRECATED. TODO
        Add or update notes related to the user.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_UpdateNotes>`__

        Args:
            user_id (str or int): The userUid of the user whose notes you want to update.
            notes (str): User profile notes.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.update(
            user_id, notes=notes, path=["notes"]
        )

    def add_user_risk_tags(self, user_id, tags):
        """DEPRECATED. TODO
        Add one or more risk factor tags.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_AddRiskFactors>`__

        Args:
            user_id (str or int): The userUid of the user whose risk factor tag(s) you want to update.
            tags (str or list of str ): A single tag or multiple tags in a list to be added. For
                example: ``"tag1"`` or ``["tag1", "tag2"]``.

                Constants available at :class:`py42.constants.RiskTags`

        Returns:
            :class:`py42.response.Py42Response`
        """
        if not isinstance(tags, (list, tuple)):
            tags = [tags]
        for tag in tags:
            self._watchlist_service.add_included_users_by_watchlist_type([user_id], tag)

    def remove_user_risk_tags(self, user_id, tags):
        """DEPRECATED. TODO
        Remove one or more risk factor tags.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_RemoveRiskFactors>`__

        Args:
            user_id (str or int): The userUid of the user whose risk factor tag(s) needs you want to remove.
            tags (str or list of str ): A single tag or multiple tags in a list to be removed. For
                example: ``"tag1"`` or ``["tag1", "tag2"]``.

                Constants available at :class:`py42.constants.RiskTags`

        Returns:
            :class:`py42.response.Py42Response`
        """
        if not isinstance(tags, (list, tuple)):
            tags = [tags]
        for tag in tags:
            self._watchlist_service.delete_included_users_by_watchlist_type(
                [user_id], tag
            )

    def add_user_cloud_alias(self, user_id, alias):
        """DEPRECATED. TODO
        Add a cloud alias to a user.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_AddCloudUsernames>`__

        Args:
            user_id (str or int): The userUid of the user whose alias you want to update.
            alias (str): The alias to be added.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.add_cloud_aliases(user_id, [alias])

    def remove_user_cloud_alias(self, user_id, alias):
        """DEPRECATED. TODO
        Remove a cloud alias from a user.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_RemoveCloudUsernames>`__

        Args:
            user_id (str or int): The userUid of the user whose alias needs to be removed.
            alias (str): The alias to be removed.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.delete_cloud_aliases(user_id, [alias])

    def refresh_user_scim_attributes(self, user_id):
        # TODO: does this have a new API
        """Refresh SCIM attributes of a user.
        `Rest Documentation <https://developer.code42.com/api/#operation/UserControllerV2_RefreshUser>`__

        Args:
            user_id (str or int): The userUid of the user whose attributes you wish to refresh.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.refresh(user_id)
