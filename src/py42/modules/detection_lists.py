class DetectionListsModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory

    @property
    def departing_employee(self):
        return self._microservice_client_factory.get_departing_employee_client()
