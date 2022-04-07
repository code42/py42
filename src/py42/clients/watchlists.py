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
    * ``SUSPICIOUS_SYSTEM_ACTIVITY``"
    """

    CONTRACT_EMPLOYEE = "CONTRACT_EMPLOYEE"
    DEPARTING_EMPLOYEE = "DEPARTING_EMPLOYEE"
    ELEVATED_ACCESS_PRIVILEGES = "ELEVATED_ACCESS_PRIVILEGES"
    FLIGHT_RISK = "FLIGHT_RISK"
    HIGH_IMPACT_EMPLOYEE = "HIGH_IMPACT_EMPLOYEE"
    NEW_EMPLOYEE = "NEW_EMPLOYEE"
    PERFORMANCE_CONCERNS = "PERFORMANCE_CONCERNS"
    POOR_SECURITY_PRACTICES = "POOR_SECURITY_PRACTICES"
    SUSPICIOUS_SYSTEM_ACTIVITY = "SUSPICIOUS_SYSTEM_ACTIVITY"


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

    def list(self, page=None, page_size=None):
        """Get a page of watchlists.

        Args:
                page (integer, optional): The desired page of watchlist results to retrieve.  Defaults to None
                page_size (integer, optional): The desired number of results per page.  Defaults to None

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.list(page, page_size)

    def create(self, watchlist_type):
        """Create a new watchlist.

        Args:
                watchlist_type (str): Type of watchlist. Constants available at :class:`py42.constants.WatchlistType`.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.create(watchlist_type)

    def get_page_included_users(self, watchlist_id, page=None, page_size=None):
        """Get page of users explicitly included on a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.
                page (integer, optional): The desired page of included users to retrieve.  Defaults to None
                page_size (integer, optional): The desired number of results per page.  Defaults to None

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.get_page_included_users(
            watchlist_id, page, page_size
        )

    def get_all_included_users(self, watchlist_id):
        """Get all users explicitly included on a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.

        Returns:
                :class:`py42.response.Py42Response`
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
        return self._watchlists_service.add_included_users_by_watchlist_type(
            user_ids, watchlist_type
        )

    def delete_included_users_by_watchlist_id(self, user_ids, watchlist_id):
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

    def delete_included_users_by_watchlist_type(self, user_ids, watchlist_type):
        """Remove users that are explicitly included on a watchlist.

        Args:
                user_ids (list(str): A list of user IDs to remove from the watchlist
                watchlist_type (str): Type of watchlist. Constants available at :class:`py42.constants.WatchlistType`.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.delete_included_users_by_watchlist_type(
            user_ids, watchlist_type
        )

    def get_page_watchlist_members(self, watchlist_id, page=None, page_size=None):
        """Get a page of all members of a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.
                page (integer, optional): The desired page of members to retrieve.  Defaults to None
                page_size (integer, optional): The desired number of results per page.  Defaults to None

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._watchlists_service.get_page_watchlist_members(
            watchlist_id, page, page_size
        )

    def get_all_watchlist_members(self, watchlist_id):
        """Get all members of a watchlist.

        Args:
                watchlist_id (str): A unique watchlist ID.

        Returns:
                :class:`py42.response.Py42Response`
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
