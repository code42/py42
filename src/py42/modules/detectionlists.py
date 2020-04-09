class DetectionListsModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory

    @property
    def departing_employee(self):
        return self._microservice_client_factory.get_departing_employee_client()

    @property
    def high_risk_employee(self):
        return self._microservice_client_factory.get_high_risk_employee_client()

    def update_notes(self, user_id, notes):
        # Need to figure out how detection_list_user_client will be instantiated
        self._detection_list_user_client.update_notes(user_id, notes)

    def add_risk_tag(self, user_id, tags):
        # Below note applies to `remove_risk_tag`, `add_cloud_alias`, `remove_cloud_alias` as well.

        # Changed method signature, used 'tags' instead of 'tag' as compared to requirement,
        # as the API expects a list.

        # Suggestion:
        # we can allow user to pass either of string or list and manage it on our side as
        # below, i.e if its not a list, make a list and pass it to the API.
        # if type(tags) is str:
        #   tags = [tags]

        # I don't see much validation done in other modules as well, do we need to add
        # validation, whether tags is None then return or throw error?

        self._detection_list_user_client.add_risk_tag(user_id, tags)

    def remove_risk_tag(self, user_id, tags):
        self._detection_list_user_client.remove_risk_tag(user_id, tags)

    def add_cloud_alias(self, user_id, aliases):
        self._detection_list_user_client.add_cloud_alias(user_id, aliases)

    def remove_cloud_alias(self, user_id, aliases):
        self._detection_list_user_client.remove_cloud_alias(user_id, aliases)
