import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages
from py42.sdk.exceptions import Py42NotFoundError


class HighRiskEmployeeClient(BaseClient):
    """
    TODO Documentation here
    """

    # In other modules URI is a single variable, breaking it up to have better control
    # if we want to refactor version and prefix to a common configuration.
    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}".format(_api_version)

    def __init__(self, session, user_context):
        super(HighRiskEmployeeClient, self).__init__(session)
        self._user_context = user_context

    def _create_user(self, username, tenant_id, risk_factors=None, note=None, cloud_aliases=None):
        resource = u"/user/create"
        uri = u"{0}{1}".format(self._uri_prefix, resource)

        cloud_aliases = cloud_aliases if cloud_aliases else []
        risk_factors = risk_factors if risk_factors else []
        data = {
            "tenantId": tenant_id,
            "userName": username,
            "notes": note,
            "riskFactors": risk_factors,
            "cloudUsernames": cloud_aliases,
        }
        return self._session.post(uri, data=json.dumps(data))

    def _add_high_risk_employee(self, tenant_id, user_id):
        data = {"tenantId": tenant_id, "userId": user_id}
        resource = u"/highriskemployee/add"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def create(self, username, risk_factors=None, note=None, cloud_aliases=None):
        """
        Creates a user under detection list and add it to high risk employee lens.

        If user already exists, add to high risk lens, else create and add.
        """
        tenant_id = self._user_context.get_current_tenant_id()
        try:
            user_response = self.get_by_username(username)
        except Py42NotFoundError:
            user_response = self._create_user(
                username,
                tenant_id,
                risk_factors=risk_factors,
                note=note,
                cloud_aliases=cloud_aliases,
            )

        user_id = user_response["userId"]
        return self._add_high_risk_employee(tenant_id, user_id)

    def toggle_alerts(self, alerts_enabled=True):
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "alertsEnabled": alerts_enabled,
        }
        resource = u"/highriskemployee/setalertstate"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def resolve(self, user_id):
        data = {"tenantId": self._user_context.get_current_tenant_id(), "userId": user_id}
        resource = u"/highriskemployee/remove"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get_by_id(self, user_id):
        data = {"tenantId": self._user_context.get_current_tenant_id(), "userId": user_id}
        resource = u"/user/getbyid"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get_by_username(self, username):
        data = {"tenantId": self._user_context.get_current_tenant_id(), "username": username}
        resource = u"/user/getbyusername"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def _get_high_risk_employees_page(
        self,
        tenant_id,
        risk_factors,
        filter_type,
        sort_key,
        sort_direction,
        page_size=100,
        page_num=1,
    ):
        # Did not define default values for sort_key, sort_direction as they would have
        # a value defined by the calling function. Or do we need it?!

        data = {
            "tenantId": tenant_id,
            "filterType": filter_type,
            "riskFactors": risk_factors,
            "pgSize": page_size,
            "pgNum": page_num,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        resource = u"/highriskemployee/search"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get_all(
        self,
        tenant_id=None,
        risk_factors=None,
        filter_type="OPEN",
        sort_key="createdAt",
        sort_direction="DESC",
    ):
        return get_all_pages(
            self._get_high_risk_employees_page,
            "items",
            tenant_id=tenant_id,
            risk_factors=risk_factors,
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )


class DetectionListUserClient(BaseClient):
    """
    TODO Documentation here
    """

    # TODO Confirm whether DetectionList is redundant since it will be
    # called as sdk.detectionlist.DetectionListUserClient

    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}/user".format(_api_version)

    def __init__(self, session, user_context):
        super(DetectionListUserClient, self).__init__(session)
        self._user_context = user_context

    def update_notes(self, user_id, note):

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "notes": note,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"updatenotes")
        return self._session.post(uri, data=json.dumps(data))

    def add_risk_tag(self, user_id, risk_factors=None):

        risk_factors = risk_factors if risk_factors else []
        # should we return if risk_factors is empty?
        # if so, in that case the response would not be a Py42Response, or should we create it?
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": risk_factors,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"addriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def remove_risk_tag(self, user_id, risk_factors):
        risk_factors = risk_factors if risk_factors else []
        # should we return,  if risk_factors is empty?
        # if so, in that case the response would not be a Py42Response, or should we create it?
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": risk_factors,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"removeriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def add_cloud_alias(self, user_id, cloud_aliases=None):
        cloud_aliases = cloud_aliases if cloud_aliases else []

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": cloud_aliases,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"addcloudusernames")
        return self._session.post(uri, data=json.dumps(data))

    def remove_cloud_alias(self, user_id, cloud_aliases):
        cloud_aliases = cloud_aliases if cloud_aliases else []

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": cloud_aliases,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"removecloudusernames")
        return self._session.post(uri, data=json.dumps(data))
