import json

from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)
from py42._internal.clients.administration import AdministrationClient
from py42.util import get_obj_from_response


class DepartingEmployeeModule(object):
    _tenant_id = None

    class DepartingEmployeeSearchFilter(object):
        OPEN = "OPEN"
        LEAVING_TODAY = "LEAVING_TODAY"
        EXFILTRATION_24_HOURS = "EXFILTRATION_24_HOURS"
        EXFILTRATION_30_DAYS = "EXFILTRATION_30_DAYS"

    def __init__(self, administration_client, departing_employee_client):
        # type: (AdministrationClient, DepartingEmployeeClient) -> None
        self._administration = administration_client
        self._departing_employee_client = departing_employee_client
        self._tenant_id = self._get_tenant_id()

    def create_departing_employee(
        self,
        username,
        tenant_id=None,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        cloud_usernames=None,
    ):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.create_departing_employee(
            username=username,
            tenant_id=tenant_id,
            notes=notes,
            departure_date=departure_date,
            alerts_enabled=alerts_enabled,
            cloud_usernames=cloud_usernames,
        )

    def resolve_case_by_username(self, username):
        case_id = self._get_case_id_from_username(username)
        return self.resolve_case_by_id(case_id)

    def resolve_case_by_id(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.resolve_departing_employee(tenant_id, case_id)

    def search_departing_employees(
        self,
        tenant_id=None,
        page_size=100,
        page_num=1,
        departing_on_or_after=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.search_departing_employees(
            tenant_id=tenant_id,
            page_size=page_size,
            page_num=page_num,
            departing_on_or_after=departing_on_or_after,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def search_departing_employees_with_filter(
        self,
        filter_type,
        tenant_id=None,
        page_size=100,
        page_num=1,
        departing_on_or_after=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.search_departing_employees_with_filter(
            tenant_id=tenant_id,
            filter_type=filter_type,
            page_size=page_size,
            page_num=page_num,
            departing_on_or_after=departing_on_or_after,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def toggle_alerts(self, alerts_enabled, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.toggle_alerts(tenant_id, alerts_enabled)

    def validate_user(self, username, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.validate_user(username, tenant_id)

    def get_details_by_username(self, username):
        case_id = self._get_case_id_from_username(username)
        return self.get_details_by_case_id(case_id)

    def get_details_by_case_id(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        return self._departing_employee_client.get_case_details(tenant_id, case_id)

    def update_case_by_username(
        self,
        username,
        tenant_id=None,
        display_name=None,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        status="OPEN",
        cloud_usernames=None,
    ):
        case_id = self._get_case_id_from_username(username)
        return self.update_case_by_id(
            case_id=case_id,
            tenant_id=tenant_id,
            display_name=display_name,
            notes=notes,
            departure_date=departure_date,
            alerts_enabled=alerts_enabled,
            status=status,
            cloud_usernames=cloud_usernames,
        )

    def update_case_by_id(
        self,
        case_id,
        tenant_id=None,
        display_name=None,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        status="OPEN",
        cloud_usernames=None,
    ):
        tenant_id = tenant_id if tenant_id else self._tenant_id
        display_name = (
            display_name if display_name else self._get_display_name_from_case_id(case_id)
        )
        return self._departing_employee_client.update_case(
            tenant_id=tenant_id,
            case_id=case_id,
            display_name=display_name,
            notes=notes,
            departure_date=departure_date,
            alerts_enabled=alerts_enabled,
            status=status,
            cloud_usernames=cloud_usernames,
        )

    def _get_tenant_id(self):
        response = self._administration.get_current_tenant()
        tenant = get_obj_from_response(response, u"data")
        return tenant.get(u"tenantUid")

    def _get_case_id_from_username(self, username):
        response = self.search_departing_employees().text
        cases = json.loads(response).get(u"cases")
        for case in cases:
            case_user = case.get(u"userName")
            if case.get(u"type$") == u"DEPARTING_EMPLOYEE_CASE" and case_user == username:
                return case.get(u"caseId")

    def _get_display_name_from_case_id(self, case_id):
        response = self.search_departing_employees().text
        cases = json.loads(response).get(u"cases")
        for case in cases:
            this_case_id = case.get(u"caseId")
            if case.get(u"type$") == u"DEPARTING_EMPLOYEE_CASE" and this_case_id == case_id:
                return case.get(u"displayName")
