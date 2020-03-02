from py42._internal.client_factories import EmployeeCaseManagementClientFactory


class EmployeeCaseManagementModule(object):
    def __init__(self, microservice_client_factory):
        self._microservice_client_factory = microservice_client_factory
        self._departing_employee_client = None

    @property
    def departing_employee(self):
        if not self._departing_employee_client:
            self._departing_employee_client = (
                self._microservice_client_factory.create_departing_employee_client()
            )
        return self._departing_employee_client
