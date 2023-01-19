from py42.exceptions import Py42Error
from py42.exceptions import Py42NotFoundError


class UserRiskProfileClient:
    """A client to expose the user risk profile API.

    `Rest Documentation <https://developer.code42.com/api/#tag/User-Risk-Profiles>`__
    """

    def __init__(self, user_risk_profile_service, user_service):
        self._user_risk_profile_service = user_risk_profile_service
        self._user_service = user_service

    def get_by_id(self, user_id):
        """Get a user risk profile by a user UID.

        Args:
                user_id (str): A unique user UID.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.get_by_id(user_id)

    def get_by_username(self, username):
        """Get a user risk profile by username.

        Args:
                username (str): A username.

        Returns:
                :class:`py42.response.Py42Response`
        """
        user_response = self._user_service.get_by_username(username)
        if len(user_response.data["users"]) == 0:
            err = Py42Error()
            err.response = user_response
            raise Py42NotFoundError(err, message=f"Username '{username}' not found.")
        user_id = user_response.data["users"][0]["userUid"]
        return self.get_by_id(user_id)

    def update(self, user_id, start_date=None, end_date=None, notes=None):
        """Update a user risk profile.

        For each arg, if None is provided, the value will not be updated. Pass an empty string if you want to clear that value from the profile.

        Args:
                user_id (str): The UID of the user to update.
                start_date (str or datetime, optional): The start date of the user risk profile to be updated. Expects format of 'YYYY-MM-DD' or instance of datetime. Defaults to None.
                end_date (str or datetime, optional): The departure date of the user risk profile to be updated. Expects format of 'YYYY-MM-DD' or instance of datetime. Defaults to None.
                notes (str, optional): The notes field of the user risk profile to be updated. Defaults to None

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.update(
            user_id, start_date, end_date, notes
        )

    def get_page(
        self,
        page_num=1,
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
                page_num (integer, optional): The desired page of user risk profile results to retrieve.  Defaults to None
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
            page_num,
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
                user_id (str): The user UID.
                cloud_alias (str or list(str)): The alias(es) to add to the user risk profile. Each user starts with a default alias of their code42 username and can have one additional cloud alias.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.add_cloud_aliases(user_id, cloud_alias)

    def delete_cloud_aliases(self, user_id, cloud_aliases):
        """Delete cloud aliases from a user risk profile.

        Args:
                user_id (str): The user UID.
                cloud_aliases (str or list(str)): The alias(es) to remove from the user risk profile. Each user starts with a default alias of their code42 username and can have one additional cloud alias.

        Returns:
                :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.delete_cloud_aliases(
            user_id, cloud_aliases
        )
