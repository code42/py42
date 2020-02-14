import json

from py42._internal.base_classes import BaseClient


class DepartingEmployeeClient(BaseClient):
    _uri_prefix =  u"/svc/api/v1/departingemployee/{0}"
    _tenant_id = None

    def __init__(self, session, administration_client):
        super(DepartingEmployeeClient, self).__init__(session)
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
        uri = self._uri_prefix.format(u"create")
        return self._default_session.post(uri, data=json.dumps(data))

    def resolve_departing_employee(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._uri_prefix.format(u"resolve")
        data = {u"caseId": case_id, u"tenantId": tenant_id}
        return self._default_session.post(uri, data=json.dumps(data))

    def get_all_departing_employees(
        self,
        tenant_id=None,
        page_size=100,
        page_num=1,
        departing_on_or_after=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._uri_prefix.format(u"search")
        data = {
            u"tenantId": tenant_id,
            u"pgSize": page_size,
            u"pgNum": page_num,
            u"departingOnOrAfter": departing_on_or_after,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._default_session.post(uri, data=json.dumps(data))

    def toggle_alerts(self, tenant_id=None, alerts_enabled=True):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._uri_prefix.format(u"togglealerts")
        data = {u"tenantId": tenant_id, u"alertsEnabled": alerts_enabled}
        return self._default_session.post(uri, data=json.dumps(data))

    def get_case_by_username(self, username, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        case_id = self._get_case_id_from_username(tenant_id, username)
        return self.get_case_by_id(case_id, tenant_id)

    def get_case_by_id(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._uri_prefix.format(u"details")
        data = {u"tenantId": tenant_id, u"caseId": case_id}
        return self._default_session.post(uri, data=json.dumps(data))

    def update_case(
        self,
        case_id,
        tenant_id=None,
        display_name=None,
        notes=None,
        departure_date=None,
        alerts_enabled=None,
        status=None,
        cloud_usernames=None,
    ):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()

        # The behavior of this API is to clear values that are not provided.
        # Therefore, we check current values first as to prevent clearing them when not provided.
        # departureDate is not cleared, however.

        # Cannot use `self.get_case_by_id()` here because
        # it does not include cloudUsername or departureDate
        case = self._get_case_from_id(tenant_id, case_id)

        if display_name is None:
            display_name = case.get(u"displayName")

        if notes is None:
            notes = case.get(u"notes")

        if departure_date is None:
            departure_date = case.get(u"departureDate")

        if alerts_enabled is None:
            current_alerts_enabled = case.get(u"alertsEnabled")
            alerts_enabled = current_alerts_enabled if current_alerts_enabled else True

        if status is None:
            current_status = case.get(u"status")
            status = current_status if current_status else u"OPEN"

        if cloud_usernames is None:
            current_cloud_usernames = case.get(u"cloudUsernames")
            cloud_usernames = current_cloud_usernames if current_cloud_usernames else []

        uri = self._uri_prefix.format(u"update")
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
        return self._default_session.post(uri, data=json.dumps(data))

    def _get_current_tenant_id(self):
        if self._tenant_id is None:
            self._tenant_id = self._administration.get_current_tenant_id()
        return self._tenant_id

    def _get_case_id_from_username(self, tenant_id, username):
        case = self._get_case_from_username(tenant_id, username)
        if case is not None:
            return case.get(u"caseId")

    def _get_case_from_username(self, tenant_id, username):
        return self._get_case_from_key(tenant_id, u"userName", username)

    def _get_case_from_id(self, tenant_id, case_id):
        return self._get_case_from_key(tenant_id, u"caseId", case_id)

    def _get_case_from_key(self, tenant_id, key, value_in_sought_case):
        cases = self._get_all_departing_employees(tenant_id)
        for case in cases:
            case_value = case.get(key)
            if (
                case.get(u"type$") == u"DEPARTING_EMPLOYEE_CASE"
                and case_value == value_in_sought_case
            ):
                return case

    def _get_all_departing_employees(self, tenant_id):
        response = self.get_all_departing_employees(tenant_id).text
        return json.loads(response).get(u"cases")
