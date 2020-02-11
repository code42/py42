import json

from py42._internal.base_classes import BaseEmployeeCaseManagementClient
from py42.util import get_obj_from_response


class DepartingEmployeeClient(BaseEmployeeCaseManagementClient):
    _base_uri = "/svc/api/v1/departingemployee/"
    _tenant_id = None

    def __init__(self, session, administration_client):
        super().__init__(session)
        self._administration = administration_client

    def create_departing_employee(
        self,
        username,
        tenant_id=None,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        cloud_usernames=None,
    ):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        cloud_usernames = cloud_usernames if cloud_usernames else []
        data = {
            u"userName": username,
            u"tenantId": tenant_id,
            u"notes": notes,
            u"departureDate": departure_date,
            u"alertsEnabled": alerts_enabled,
            u"cloudUsernames": cloud_usernames,
        }
        uri = u"{0}create".format(self._base_uri)
        return self._session.post(uri, data=json.dumps(data))

    def resolve_departing_employee(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = u"{0}resolve".format(self._base_uri)
        data = {u"caseId": case_id, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))

    def get_all_departing_employees(
        self,
        tenant_id=None,
        page_size=100,
        page_num=1,
        departing_on_or_after=None,
        sort_key="CREATED_AT",
        sort_direction="DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._get_uri(u"search")
        data = {
            u"tenantId": tenant_id,
            u"pgSize": page_size,
            u"pgNum": page_num,
            u"departingOnOrAfter": departing_on_or_after,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._session.post(uri, data=json.dumps(data))

    def search_departing_employees(
        self,
        tenant_id=None,
        filter_type="OPEN",
        page_size=1,
        page_num=100,
        departing_on_or_after=None,
        sort_key="CREATED_AT",
        sort_direction="DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._get_uri(u"filteredsearch")
        data = {
            u"tenantId": tenant_id,
            u"filterType": filter_type,
            u"pgSize": page_size,
            u"pgNum": page_num,
            u"departingOnOrAfter": departing_on_or_after,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._session.post(uri, data=json.dumps(data))

    def toggle_alerts(self, tenant_id=None, alerts_enabled=True):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._get_uri(u"togglealerts")
        data = {u"tenantId": tenant_id, u"alertsEnabled": alerts_enabled}
        return self._session.post(uri, data=json.dumps(data))

    def get_case_by_username(self, username, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        case_id = self._get_case_id_from_username(tenant_id, username)
        return self.get_case_by_id(case_id, tenant_id)

    def get_case_by_id(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._get_uri(u"details")
        data = {u"tenantId": tenant_id, u"caseId": case_id}
        return self._session.post(uri, data=json.dumps(data))

    def update_case(
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
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        display_name = (
            display_name if display_name else self._get_display_name_from_case_id(tenant_id, case_id)
        )
        uri = self._get_uri(u"update")
        cloud_usernames = cloud_usernames if cloud_usernames else []
        data = {
            u"tenantId": tenant_id,
            u"caseId": case_id,
            u"displayName": display_name,
            u"notes": notes,
            u"departureDate": departure_date,
            u"alertsEnabled": alerts_enabled,
            u"status": status,
            u"cloudUsernames": cloud_usernames,
        }
        return self._session.post(uri, data=json.dumps(data))

    def _get_uri(self, resource_name):
        return u"{0}{1}".format(self._base_uri, resource_name)

    def _get_current_tenant_id(self):
        if self._tenant_id is None:
            response = self._administration.get_current_tenant()
            tenant = get_obj_from_response(response, u"data")
            self._tenant_id = tenant.get(u"tenantUid")
        return self._tenant_id

    def _get_case_id_from_username(self, tenant_id, username):
        response = self.get_all_departing_employees(tenant_id).text
        cases = json.loads(response).get(u"cases")
        for case in cases:
            case_user = case.get(u"userName")
            if case.get(u"type$") == u"DEPARTING_EMPLOYEE_CASE" and case_user == username:
                return case.get(u"caseId")

    def _get_display_name_from_case_id(self, tenant_id, case_id):
        response = self.get_all_departing_employees(tenant_id).text
        cases = json.loads(response).get(u"cases")
        for case in cases:
            this_case_id = case.get(u"caseId")
            if case.get(u"type$") == u"DEPARTING_EMPLOYEE_CASE" and this_case_id == case_id:
                return case.get(u"displayName")
