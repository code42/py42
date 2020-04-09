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

    def _create_user(self, username, tenant_id):
        resource = u"/user/create"
        uri = u"{0}{1}".format(self._uri_prefix, resource)

        data = {
            "tenantId": tenant_id,
            "userName": username,
        }
        return self._session.post(uri, data=json.dumps(data))

    def _add_high_risk_employee(self, tenant_id, user_id):

        data = {"tenantId": tenant_id, "userId": user_id}
        resource = u"/highriskemployee/add"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def add(self, user_id=None, username=None):
        """
        Adds a user to high risk employee lens, optionally creates a user if it doesn't exist.

        If `user_id` is not available, pass `username` parameter, new user will be
        created and added to high risk employee lens.

        Args: Either of user_id or username must be defined.
        TODO
        """
        tenant_id = self._user_context.get_current_tenant_id()
        if user_id:
            return self._add_high_risk_employee(tenant_id, user_id)
        if username:
            try:
                user_response = self._get_by_username(username)
            except Py42NotFoundError:
                user_response = self._create_user(username, tenant_id,)
            user_id = user_response["userId"]
            return self._add_high_risk_employee(tenant_id, user_id)

        # TODO # Waiting on CustomError name?!!
        # raise CustomPy42Error("Either of user_id or username must be defined.")

    def set_alerts_enabled(self, enabled=True):
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "alertsEnabled": enabled,
        }
        resource = u"/highriskemployee/setalertstate"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def remove(self, user_id):
        data = {"tenantId": self._user_context.get_current_tenant_id(), "userId": user_id}
        resource = u"/highriskemployee/remove"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get(self, user_id):
        data = {"tenantId": self._user_context.get_current_tenant_id(), "userId": user_id}
        resource = u"/user/getbyid"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def _get_by_username(self, username):
        # Made this as private method as it is not required as per requirement doc.
        # This method is needed to check user existence, during create.
        data = {"tenantId": self._user_context.get_current_tenant_id(), "username": username}
        resource = u"/user/getbyusername"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def _get_high_risk_employees_page(
        self, risk_tags, filter_type, sort_key, sort_direction, page_size, page_num,
    ):

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "filterType": filter_type,
            "riskFactors": risk_tags,
            "pgSize": page_size,
            "pgNum": page_num,
        }
        if sort_key:
            data["srtKey"] = sort_key
        if sort_direction:
            data["srtDirection"] = sort_direction

        resource = u"/highriskemployee/search"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get_all(
        self,
        risk_tags=None,
        filter_type="OPEN",
        sort_key=None,
        sort_direction=None,
        page_size=100,
        page_num=1,
    ):
        """
        Search High Risk employee list. Filter results by filter_type or risk factors.

        #TODO Param description
        """

        return get_all_pages(
            self._get_high_risk_employees_page,
            "items",
            risk_tags=risk_tags,
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_size=page_size,
            page_num=page_num,
        )


class DetectionListUserClient(BaseClient):
    """
    TODO Documentation here
    """

    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}/user".format(_api_version)

    def __init__(self, session, user_context):
        super(DetectionListUserClient, self).__init__(session)
        self._user_context = user_context

    def update_notes(self, user_id, notes):

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "notes": notes,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"updatenotes")
        return self._session.post(uri, data=json.dumps(data))

    def add_risk_tag(self, user_id, tags):

        tags = tags if tags else []
        # TODO Return Error when user_id or tags is not defined. Similarly for all other
        # methods below
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": tags,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"addriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def remove_risk_tag(self, user_id, tags):
        tags = tags if tags else []

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": tags,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"removeriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def add_cloud_alias(self, user_id, aliases):
        aliases = aliases if aliases else []

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": aliases,
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
