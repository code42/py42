from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)


class EmployeeCaseManagementModule(object):
    def __init__(self, departing_employee_client):
        # type: (EmployeeCaseManagementModule, DepartingEmployeeClient) -> None
        self.departing_employee = departing_employee_client
