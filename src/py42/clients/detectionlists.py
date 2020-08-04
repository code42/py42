class DetectionListsModule(object):
    def __init__(self, user_profile_service, departing_employee_service, high_risk_employee_service):
        self._user_profile_service = user_profile_service
        self._departing_employee_service = departing_employee_service
        self._high_risk_employee_service = high_risk_employee_service

    @property
    def departing_employee(self):
        return self._departing_employee_service

    @property
    def high_risk_employee(self):
        return self._high_risk_employee_service

    def create_user(self, username):
        """Create a detection list profile for a user.

        Args:
            username (str): The Code42 username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.create(username)

    def get_user(self, username):
        """Get user details by username.

        Args:
            username (str): The Code42 username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.get(username)

    def get_user_by_id(self, user_id):
        """Get user details by user_id.

        Args:
            user_id (str or int): The Code42 userId of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.get_by_id(user_id)

    def update_user_notes(self, user_id, notes):
        """Add or update notes related to the user.

        Args:
            user_id (str or int): The userUid of the user whose notes you want to update.
            notes (str): User profile notes.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.update_notes(user_id, notes)

    def add_user_risk_tags(self, user_id, tags):
        """Add one or more risk factor tags.

        Args:
            user_id (str or int): The userUid of the user whose risk factor tag(s) you want to update.
            tags (str or list of str ): A single tag or multiple tags in a list to be added. For
                example: ``"tag1"`` or ``["tag1", "tag2"]``. For python version 2.X, pass ``u"str"``
                instead of ``"str"``.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.add_risk_tags(user_id, tags)

    def remove_user_risk_tags(self, user_id, tags):
        """Remove one or more risk factor tags.

        Args:
            user_id (str or int): The userUid of the user whose risk factor tag(s) needs you want to remove.
            tags (str or list of str ): A single tag or multiple tags in a list to be removed. For
                example: ``"tag1"`` or ``["tag1", "tag2"]``. For python version 2.X, pass ``u"str"``
                instead of ``"str"``.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.remove_risk_tags(user_id, tags)

    def add_user_cloud_alias(self, user_id, alias):
        """Add a cloud alias to a user.

        Args:
            user_id (str or int): The userUid of the user whose alias you want to update.
            alias (str): The alias to be added.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.add_cloud_alias(user_id, alias)

    def remove_user_cloud_alias(self, user_id, alias):
        """Remove a cloud alias from a user.

        Args:
            user_id (str or int): The userUid of the user whose alias needs to be removed.
            alias (str): The alias to be removed.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.remove_cloud_alias(user_id, alias)

    def refresh_user_scim_attributes(self, user_id):
        """Refresh SCIM attributes of a user.
        `REST documentation <https://ecm-default.prod.ffs.us2.code42.com/svc/swagger/index.html?urls.primaryName=v2#/User/UserControllerV2_RefreshUser>`__

        Args:
            user_id (str or int): The userUid of the user whose attributes you wish to refresh.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_profile_service.refresh(user_id)
