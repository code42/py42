class DetectionListsModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory
        self._detection_list_user_client = None
        # TODO Fix
        # As this below code is failing, had to add a check in all the methods.
        # self._detection_list_user_client = (
        #     self._microservice_client_factory.get_detection_list_user_client()
        # )

    @property
    def departing_employee(self):
        return self._microservice_client_factory.get_departing_employee_client()

    @property
    def high_risk_employee(self):
        return self._microservice_client_factory.get_high_risk_employee_client()

    def update_notes(self, user_id, notes):
        # TODO Refactor, this condition should not be needed, relates to TODO fix above
        if not self._detection_list_user_client:
            self._detection_list_user_client = (
                self._microservice_client_factory.get_detection_list_user_client()
            )

        self._detection_list_user_client.update_notes(user_id, notes)

    def add_risk_tag(self, user_id, tags):
        if not self._detection_list_user_client:
            self._detection_list_user_client = (
                self._microservice_client_factory.get_detection_list_user_client()
            )

        self._detection_list_user_client.add_risk_tag(user_id, tags)

    def remove_risk_tag(self, user_id, tags):
        if not self._detection_list_user_client:
            self._detection_list_user_client = (
                self._microservice_client_factory.get_detection_list_user_client()
            )

        self._detection_list_user_client.remove_risk_tag(user_id, tags)

    def add_cloud_alias(self, user_id, aliases):
        if not self._detection_list_user_client:
            self._detection_list_user_client = (
                self._microservice_client_factory.get_detection_list_user_client()
            )

        self._detection_list_user_client.add_cloud_alias(user_id, aliases)

    def remove_cloud_alias(self, user_id, aliases):
        if not self._detection_list_user_client:
            self._detection_list_user_client = (
                self._microservice_client_factory.get_detection_list_user_client()
            )

        self._detection_list_user_client.remove_cloud_alias(user_id, aliases)
