class UserRiskProfileClient:
    """A client to expose the user risk profile API.

    `Rest Documentation <https://developer.code42.com/api/#tag/User-Risk-Profiles>`__
    """

    def __init__(self, user_risk_profile_service):
        self._user_risk_profile_service = user_risk_profile_service

    def get(self, user_id):
        """Get a user risk profile.

        Args:
                user_id (str): A unique user UID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.get(user_id)

    def update(self, user_id, start_date=None, end_date=None, notes=None, paths=None):
        """Update a user risk profile.

        Args:
                user_id (str): The UID of the user to update.
                start_date (str): The start date of the user risk profile to be updated. Expects format of 'YYYY-MM-DD'. Defaults to None.
                end_date (str): The departure date of the user risk profile to be updated. Expects format of 'YYYY-MM-DD'. Defaults to None.
                notes (str): The notes field of the user risk profile to be updated. Defaults to None
                paths (list(str), optional): The set of field mask paths. Defaults to None. If None, it will assume that any provided values for ``startDate``, ``endDate``, and ``notes`` for are intended to be updated on the user risk profile. Example: ["endDate", "startDate"]

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.update(
            user_id, start_date, end_date, notes, paths
        )

    def get_page(
        self,
        page=None,
        page_size=None,
        manager_id=None,
        title=None,
        division=None,
        department=None,
        employment_type=None,
        country=None,
        region=None,
        locality=None,
        active=None,
        deleted=None,
        support_user=None,
    ):
        """Get a page of user risk profiles.

        Args:
                page (integer, optional): The desired page of user risk profile results to retrieve.  Defaults to None
                page_size (integer, optional): The desired number of results per page.  Defaults to None
                manager_id (str, optional): Matches users whose manager has the given Code42 user UID.  Defaults to None
                title (str, optional): Matches users with the given job title.  Defaults to None
                division (str, optional): Matches users in the given division.  Defaults to None
                department (str, optional): Matches users in the given department.  Defaults to None
                employment_type (str, optional): Matches users with the given employment type.  Defaults to None
                country (str, optional): Matches users in the given country.  Defaults to None
                region (str, optional): Matches users the given region (state).  Defaults to None
                locality (str, optional): Matches users in the given locality (city).  Defaults to None
                active (boolean, optional): Matches users by whether the user is active.  Defaults to None
                deleted (boolean, optional): Matches users by whether the user is deleted.  Defaults to None
                support_user (boolean, optional): Matches users by whether the user is a support user.  Defaults to None

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.get_page(
            page,
            page_size,
            manager_id,
            title,
            division,
            department,
            employment_type,
            country,
            region,
            locality,
            active,
            deleted,
            support_user,
        )

    def get_all(
        self,
        manager_id=None,
        title=None,
        division=None,
        department=None,
        employment_type=None,
        country=None,
        region=None,
        locality=None,
        active=None,
        deleted=None,
        support_user=None,
    ):
        """Get all user risk profiles.

        Args:
                manager_id (str, optional): Matches users whose manager has the given Code42 user UID.  Defaults to None
                title (str, optional): Matches users with the given job title.  Defaults to None
                division (str, optional): Matches users in the given division.  Defaults to None
                department (str, optional): Matches users in the given department.  Defaults to None
                employment_type (str, optional): Matches users with the given employment type.  Defaults to None
                country (str, optional): Matches users in the given country.  Defaults to None
                region (str, optional): Matches users the given region (state).  Defaults to None
                locality (str, optional): Matches users in the given locality (city).  Defaults to None
                active (boolean, optional): Matches users by whether the user is active.  Defaults to None
                deleted (boolean, optional): Matches users by whether the user is deleted.  Defaults to None
                support_user (boolean, optional): Matches users by whether the user is a support user.  Defaults to None

        Returns:
                generator: An object that iterates over :class:`py42.response.Py42Response` objects that each contain a page of user risk profiles.
        """
        return self._user_risk_profile_service.get_all(
            manager_id,
            title,
            division,
            department,
            employment_type,
            country,
            region,
            locality,
            active,
            deleted,
            support_user,
        )

    def add_cloud_aliases(self, user_id, cloud_alias):
        """Add cloud aliases to a user risk profile.

        Args:
                user_id (str): The UID of the user to add cloud aliases.
                cloud_alias (str or list(str)): The alias(es) to add to the user risk profile. Each user starts with a default alias of their code42 username and can have one additional cloud alias.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.add_cloud_aliases(user_id, cloud_alias)

    def delete_cloud_aliases(self, user_id, cloud_aliases):
        """Delete cloud aliases from a user risk profile.

        Args:
                user_id (str): The UID of the user to delete cloud aliases.
                cloud_aliases (str or list(str)): The alias(es) to remove from the user risk profile. Each user starts with a default alias of their code42 username and can have one additional cloud alias.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.delete_cloud_aliases(
            user_id, cloud_aliases
        )
