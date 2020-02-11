import json
from py42._internal.base_classes import BaseDetectionClient


class DepartingEmployeeClient(BaseDetectionClient):
    _base_uri = "/svc/api/v1/departingemployee/"

    def create_departing_employee(
        self,
        username,
        tenant_id,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        cloud_usernames=None,
    ):
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

    def resolve_departing_employee(self, tenant_id, case_id):
        uri = u"{0}resolve".format(self._base_uri)
        data = {u"caseId": case_id, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))

    def search_departing_employees(
        self,
        tenant_id,
        page_size=None,
        page_num=None,
        departing_on_or_after=None,
        sort_key="CREATED_AT",
        sort_direction="DESC",
    ):
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

    def search_departing_employees_with_filter(
        self,
        tenant_id,
        filter_type,
        page_size=None,
        page_num=None,
        departing_on_or_after=None,
        sort_key="CREATED_AT",
        sort_direction="DESC"
    ):
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

    def toggle_alerts(self, tenant_id, alerts_enabled):
        uri = self._get_uri(u"togglealerts")
        data = {u"tenantId": tenant_id, u"alertsEnabled": alerts_enabled}
        return self._session.post(uri, data=json.dumps(data))

    def get_case_details(self, tenant_id, case_id):
        uri = self._get_uri(u"details")
        data = {u"tenantId": tenant_id, u"caseId": case_id}
        return self._session.post(uri, data=json.dumps(data))

    def update_case(
        self,
        tenant_id,
        case_id,
        display_name,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        status="OPEN",
        cloud_usernames=None,
    ):
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

    def validate_user(self, user_name, tenant_id):
        uri = self._get_uri(u"validateuser")
        data = {u"userName": user_name, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))

    def _get_uri(self, resource_name):
        return u"{0}{1}".format(self._base_uri, resource_name)
