from py42._internal.client_factories import EmployeeCaseManagementClientFactory


class EmployeeCaseManagementModule(object):
    def __init__(self, employee_case_management_client_factory):
        # type: (EmployeeCaseManagementModule, EmployeeCaseManagementClientFactory) -> None
        self._employee_case_management_client_factory = employee_case_management_client_factory
        self._departing_employee_client = None

    @property
    def departing_employee(self):
        if self._departing_employee_client is None:
            self._departing_employee_client = (
                self._employee_case_management_client_factory.get_departing_employee_client()
            )
        return self._departing_employee_client
