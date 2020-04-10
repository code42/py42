class DetectionListsModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory
        self._detection_list_user_client = None

    @property
    def departing_employee(self):
        return self._microservice_client_factory.get_departing_employee_client()

    @property
    def high_risk_employee(self):
        return self._microservice_client_factory.get_high_risk_employee_client()

    def update_notes(self, user_id, notes):
        """Add or update notes related to the user.

        Args:
            user_id (str/int): The user_id whose notes need to be updated.
            notes (str): Note.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        self._detection_list_user_client = (
            self._microservice_client_factory.get_detection_list_user_client()
        )
        self._detection_list_user_client.update_notes(user_id, notes)

    def add_risk_tag(self, user_id, tags):
        """ Add one or more tags.

        Args:
            user_id (str/int): The user_id whose tag(s) needs to be updated.
            tags (str or list of str ): A single tag or multiple tags in a list to be added.
                e.g "tag1" or ["tag1", "tag2"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        self._detection_list_user_client = (
            self._microservice_client_factory.get_detection_list_user_client()
        )
        self._detection_list_user_client.add_risk_tag(user_id, tags)

    def remove_risk_tag(self, user_id, tags):
        """Remove one or more tags.Args:

        Args:
            user_id (str/int): The user_id whose tag(s) needs to be removed.
            tags (str or list of str ): A single tag or multiple tags in a list to be removed.
                e.g "tag1" or ["tag1", "tag2"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        self._detection_list_user_client = (
            self._microservice_client_factory.get_detection_list_user_client()
        )
        self._detection_list_user_client.remove_risk_tag(user_id, tags)

    def add_cloud_alias(self, user_id, aliases):
        """Add one or more cloud alias.

        Args:
            user_id (str/int): The user_id whose alias(es) need to be updated.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be added.
                e.g "x" or ["email@id", "y"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        self._detection_list_user_client = (
            self._microservice_client_factory.get_detection_list_user_client()
        )
        self._detection_list_user_client.add_cloud_alias(user_id, aliases)

    def remove_cloud_alias(self, user_id, aliases):
        """Remove one or more cloud alias.

        Args:
            user_id (str/int): The user_id whose alias(es) need to be removed.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be removed.
                e.g "x" or ["email@id", "y"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        self._detection_list_user_client = (
            self._microservice_client_factory.get_detection_list_user_client()
        )
        self._detection_list_user_client.remove_cloud_alias(user_id, aliases)
