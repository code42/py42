import json

from py42._internal.clients.detection.departing_employee import DepartingEmployeeClient
from py42._internal.clients.administration import AdministrationClient
from py42.util import get_obj_from_response


class DepartingEmployeeModule:
    _tenant_id = None

    def __init__(self, administration_client, departing_employee_client):
        # type: (AdministrationClient, DepartingEmployeeClient) -> None
        self._administration = administration_client
        self._departing_employee_client = departing_employee_client
        self._tenant_id = self._get_tenant_id()

    def create_departing_employee(
        self,
        user_name,
        tenant_id=None,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        cloud_user_names=None,
    ):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        cloud_user_names = cloud_user_names if cloud_user_names else []
        notes = notes if notes else ""

        return self._departing_employee_client.create_departing_employee(
            user_name, tenant_id, notes, departure_date, alerts_enabled, cloud_user_names
        )

    def resolve_departing_employee_by_username(self, user_name):
        case_id = self._get_case_id_from_user_name(user_name)
        return self.resolve_departing_employee_by_case_id(case_id)

    def resolve_departing_employee_by_case_id(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.resolve_departing_employee(case_id, tenant_id)

    def search_departing_employees(
        self,
        tenant_id=None,
        page_size="100",
        page_num="1",
        departing_on_or_after=None,
        sort_key="CREATED_AT",
        sort_direction="DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.search_departing_employees(
            tenant_id,
            page_size,
            page_num,
            departing_on_or_after,
            sort_key,
            sort_direction
        )

    def validate_user(self, user_name, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.validate_user(user_name, tenant_id)

    def _get_tenant_id(self):
        response = self._administration.get_current_tenant()
        tenant = get_obj_from_response(response, u"data")
        return tenant.get(u"tenantUid")

    def _get_case_id_from_user_name(self, user_name):
        response = self.search_departing_employees().text
        cases = json.loads(response).get(u"cases")
        for case in cases:
            case_user = case.get(u"userName")
            if case.get(u"type$") == u"DEPARTING_EMPLOYEE_CASE" and case_user == user_name:
                return case.get(u"caseId")



