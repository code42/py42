class DetectionListsModule(object):
    def __init__(self, microservice_client_factory, user_client):
        self._microservice_client_factory = microservice_client_factory
        self._user_client = user_client
        self._detection_list_user_client = None

    @property
    def departing_employee(self):
        return self._microservice_client_factory.get_departing_employee_client(self._user_client)

    @property
    def high_risk_employee(self):
        return self._microservice_client_factory.get_high_risk_employee_client(self._user_client)

    def create_user(self, username):
        """Create a detection list profile for a user.

        Args:
            username (str): The Code42 username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        return self._detection_list_user_client.create(username)

    def get_user(self, username):
        """Get user details by username.

        Args:
            username (str): The Code42 username of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        return self._detection_list_user_client.get(username)

    def get_user_by_id(self, user_id):
        """Get user details by user_id.

        Args:
            user_id (str or int): The Code42 userId of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        return self._detection_list_user_client.get_by_id(user_id)

    def update_user_notes(self, user_id, notes):
        """Add or update notes related to the user.

        Args:
            user_id (str or int): The Code42 userUid whose notes you want to update.
            notes (str): User profile notes.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        self._detection_list_user_client.update_notes(user_id, notes)

    def add_user_risk_tags(self, user_id, tags):
        """Add one or more tags.

        Args:
            user_id (str or int): The Code42 userUid whose risk factor(s) you want to update.
            tags (str or list of str ): A single risk factor or multiple risk factors in a list to
                be added. For example: ``"tag1"`` or ``["tag1", "tag2"]``. For python version 2.X,
                pass ``u"str"`` instead of ``"str"``.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        self._detection_list_user_client.add_risk_tags(user_id, tags)

    def remove_user_risk_tags(self, user_id, tags):
        """Remove one or more risk factors.

        Args:
            user_id (str or int): The Code42 userUid whose tag(s) needs you want to remove.
            tags (str or list of str ): A single risk factor or multiple risk factors in a list to
                be removed. For example: ``"tag1"`` or ``["tag1", "tag2"]``. For python version 2.X,
                pass ``u"str"`` instead of ``"str"``.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        self._detection_list_user_client.remove_risk_tags(user_id, tags)

    def add_user_cloud_aliases(self, user_id, aliases):
        """Add one or more cloud aliases.

        Args:
            user_id (str or int): The Code42 userUid whose alias(es) you want to update.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be added.
                For example: ``"x"`` or ``["email@id", "y"]``. For python version 2.X, pass ``u"str"``
                instead of ``"str"``.

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        self._detection_list_user_client.add_cloud_aliases(user_id, aliases)

    def remove_user_cloud_aliases(self, user_id, aliases):
        """Remove one or more cloud alias.

        Args:
            user_id (str or int): The user_id whose alias(es) need to be removed.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be removed.
                e.g u"x" or ["email@id", "y"], for python version 2.X, pass u"str" instead of "str"

        Returns:
            :class:`py42.response.Py42Response`
        """
        self._detection_list_user_client = self._microservice_client_factory.get_detection_list_user_client(
            self._user_client
        )
        self._detection_list_user_client.remove_cloud_aliases(user_id, aliases)
