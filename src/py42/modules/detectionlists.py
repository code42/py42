class DetectionListsModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory

    @property
    def departing_employee(self):
        return self._microservice_client_factory.get_departing_employee_client()


class HighRiskEmployeeModule(object):
    def __init__(self, detection_list_user_client, high_risk_employee_client):
        self._detection_list_user_client = detection_list_user_client
        self._high_risk_employee_client = high_risk_employee_client

    @property
    def high_risk_employee(self):
        pass
