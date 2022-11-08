from py42.choices import Choices


class WatchlistType(Choices):
    """Constants available for setting the type of watchlist.

    * ``CONTRACT_EMPLOYEE``
    * ``DEPARTING_EMPLOYEE``
    * ``ELEVATED_ACCESS_PRIVILEGES``
    * ``FLIGHT_RISK``
    * ``HIGH_IMPACT_EMPLOYEE``
    * ``NEW_EMPLOYEE``
    * ``PERFORMANCE_CONCERNS``
    * ``POOR_SECURITY_PRACTICES``
    * ``SUSPICIOUS_SYSTEM_ACTIVITY``
    * ``CUSTOM``
    """

    CONTRACTOR = "CONTRACT_EMPLOYEE"
    DEPARTING = "DEPARTING_EMPLOYEE"
    ELEVATED_ACCESS = "ELEVATED_ACCESS_PRIVILEGES"
    FLIGHT_RISK = "FLIGHT_RISK"
    HIGH_IMPACT = "HIGH_IMPACT_EMPLOYEE"
    NEW_HIRE = "NEW_EMPLOYEE"
    PERFORMANCE_CONCERNS = "PERFORMANCE_CONCERNS"
    POOR_SECURITY_PRACTICES = "POOR_SECURITY_PRACTICES"
    SUSPICIOUS_SYSTEM_ACTIVITY = "SUSPICIOUS_SYSTEM_ACTIVITY"
    CUSTOM = "CUSTOM"


class WatchlistsClient:
    """A client to expose the watchlists API.

    `Rest Documentation <https://developer.code42.com/api/#tag/Watchlists>`__
    """

    def __init__(self, watchlists_service):
        self._watchlists_service = watchlists_service

    def get(self, watchlist_id):
        """Get a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.get(watchlist_id)

    def delete(self, watchlist_id):
        """Delete a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.delete(watchlist_id)

    def get_all(self):
        """Get all watchlists.

        Returns:
                generator: An object that iterates over :class:`py42.response.Py42Response` objects that each contain a page of watchlists.
        """
        return self._watchlists_service.get_all()

    def create(self, watchlist_type, title=None, description=None):
        """Create a new watchlist.

        Args:
                watchlist_type (str): Type of watchlist. Constants available at :class:`py42.constants.WatchlistType`.
                title (str, optional): Name of watchlist (for `CUSTOM` watchlists only).
                description (str, optional): Description of watchlist (for `CUSTOM` watchlists only).

        Returns:
                :class:`py42.response.Py42Response`
        """
        if watchlist_type == "CUSTOM" and not title:
            raise ValueError("`title` value is required for custom watchlists.")
        return self._watchlists_service.create(
            watchlist_type, title=title, description=description
        )

    def get_all_included_users(self, watchlist_id):
        """Get all users explicitly included on a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.

        Returns:
                generator: An object that iterates over :class:`py42.response.Py42Response` objects that each contain a page of included users that match the given query.
        """
        return self._watchlists_service.get_all_included_users(watchlist_id)

    def add_included_users_by_watchlist_id(self, user_ids, watchlist_id):
        """Explicitly include users on a watchlist.

        Args:
                user_ids (list(str): A list of user IDs to add to the watchlist
                watchlist_id (str): A unique watchlist ID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.add_included_users_by_watchlist_id(
            user_ids, watchlist_id
        )

    def add_included_users_by_watchlist_type(self, user_ids, watchlist_type):
        """Explicitly include users on a watchlist.

        Args:
                user_ids (list(str): A list of user IDs to add to the watchlist
                watchlist_type (str): Type of watchlist. Constants available at :class:`py42.constants.WatchlistType`.

        Returns:
                :class:`py42.response.Py42Response`
        """
        if watchlist_type == "CUSTOM":
            raise ValueError(
                "Users can only be added to CUSTOM watchlists by watchlist ID."
            )
        return self._watchlists_service.add_included_users_by_watchlist_type(
            user_ids, watchlist_type
        )

    def remove_included_users_by_watchlist_id(self, user_ids, watchlist_id):
        """Remove users that are explicitly included on a watchlist.

        Args:
                user_ids (list(str): A list of user IDs to remove from the watchlist
                watchlist_id (str): A unique watchlist ID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.delete_included_users_by_watchlist_id(
            user_ids, watchlist_id
        )

    def remove_included_users_by_watchlist_type(self, user_ids, watchlist_type):
        """Remove users that are explicitly included on a watchlist.

        Args:
                user_ids (list(str): A list of user IDs to remove from the watchlist
                watchlist_type (str): Type of watchlist. Constants available at :class:`py42.constants.WatchlistType`.

        Returns:
                :class:`py42.response.Py42Response`
        """
        if watchlist_type == "CUSTOM":
            raise ValueError(
                "Users can only be removed from CUSTOM watchlists by watchlist ID."
            )
        return self._watchlists_service.delete_included_users_by_watchlist_type(
            user_ids, watchlist_type
        )

    def get_all_watchlist_members(self, watchlist_id):
        """Get all members of a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.

        Returns:
                generator: An object that iterates over :class:`py42.response.Py42Response` objects that each contain a page of watchlist members.
        """
        return self._watchlists_service.get_all_watchlist_members(watchlist_id)

    def get_watchlist_member(self, watchlist_id, user_id):
        """Get a member of a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.
                user_id (str): A unique user ID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.get_watchlist_member(watchlist_id, user_id)
