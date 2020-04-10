import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class HighRiskEmployeeClient(BaseClient):
    """
    Administrator utility to manage High Risk employees.
    `Support Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Detection_list_management_APIs>`__

    """

    # In other modules URI is a single variable, breaking it up to have better control
    # if we want to refactor version and prefix to a common configuration.
    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}".format(_api_version)

    def __init__(self, session, user_context):
        super(HighRiskEmployeeClient, self).__init__(session)
        self._user_context = user_context

    def _add_high_risk_employee(self, tenant_id, user_id):

        data = {"tenantId": tenant_id, "userId": user_id}
        resource = u"/highriskemployee/add"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def add(self, user_id=None):
        """
        Adds a user to high risk employee lens.

        If a user is already added to high risk employee lens, further attempts to add will
        return failure error.

        Args:
            user_id (str/int): Id of the user who needs to be added to HRE lens.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """

        tenant_id = self._user_context.get_current_tenant_id()
        return self._add_high_risk_employee(tenant_id, user_id)

    def set_alerts_enabled(self, enabled=True):
        """
        Enable alerts.
        #TODO Confirm
        # `toggle_alerts` would be a better method name, if we intend to allow to disable
        # alerts as well.
        Args:
            enabled (bool): Whether to enable alerts for all users

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "alertsEnabled": enabled,
        }
        resource = u"/highriskemployee/setalertstate"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def remove(self, user_id):
        """
        Remove an user from high risk employee lens.

        Args:
            user_id (str/int): Id of the user who needs to be added to HRE lens.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        data = {"tenantId": self._user_context.get_current_tenant_id(), "userId": user_id}
        resource = u"/highriskemployee/remove"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get(self, user_id):
        """
        Get user information.

        Args:
            user_id (str/int): Id of the user who needs to be added to HRE lens.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        data = {"tenantId": self._user_context.get_current_tenant_id(), "userId": user_id}
        resource = u"/user/getbyid"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def _get_high_risk_employees_page(
        self,
        tenant_id,
        filter_type=None,
        sort_key=None,
        sort_direction=None,
        page_num=None,
        page_size=None,
    ):
        # Overwriting page_size since default value 1000 returns error
        page_size = 100
        data = {
            "tenantId": tenant_id,
            "filterType": filter_type,
            "pgNum": page_num,
            "pgSize": page_size,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }

        resource = u"/highriskemployee/search"
        uri = u"{0}{1}".format(self._uri_prefix, resource)
        return self._session.post(uri, data=json.dumps(data))

    def get_all(
        self, filter_type="OPEN", sort_key=None, sort_direction=None,
    ):
        """
        Search High Risk employee list. Filter results by filter_type

        Args:
            filter_type (str): Valid filter types.
            sort_key (str): Sort results based by field.
            sort_direction (str): "ASC" or "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of users.
        """

        return get_all_pages(
            self._get_high_risk_employees_page,
            "items",
            tenant_id=self._user_context.get_current_tenant_id(),
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )


class DetectionListUserClient(BaseClient):
    """
    Administrator utility to manage High Risk employees information.
    `Support Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Detection_list_management_APIs>`__
    """

    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{0}/user".format(_api_version)

    def __init__(self, session, user_context):
        super(DetectionListUserClient, self).__init__(session)
        self._user_context = user_context

    def update_notes(self, user_id, notes):
        """Add or update notes related to the user.

        Args:
            user_id (str/int): The user_id whose notes need to be updated.
            notes (str): Note.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "notes": notes,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"updatenotes")
        return self._session.post(uri, data=json.dumps(data))

    def add_risk_tag(self, user_id, tags):
        """ Add one or more tags.

        Args:
            user_id (str/int): The user_id whose tag(s) needs to be updated.
            tags (str or list of str ): A single tag or multiple tags in a list to be added.
                e.g "tag1" or ["tag1", "tag2"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """

        if type(tags) is str:
            tags = [tags]

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": tags,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"addriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def remove_risk_tag(self, user_id, tags):
        """Remove one or more tags.Args:

        Args:
            user_id (str/int): The user_id whose tag(s) needs to be removed.
            tags (str or list of str ): A single tag or multiple tags in a list to be removed.
                e.g "tag1" or ["tag1", "tag2"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        if type(tags) is str:
            tags = [tags]

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "riskFactors": tags,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"removeriskfactors")
        return self._session.post(uri, data=json.dumps(data))

    def add_cloud_alias(self, user_id, aliases):
        """Add one or more cloud alias.

        Args:
            user_id (str/int): The user_id whose alias(es) need to be updated.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be added.
                e.g "x" or ["email@id", "y"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        if type(aliases) is str:
            aliases = [aliases]

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": aliases,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"addcloudusernames")
        return self._session.post(uri, data=json.dumps(data))

    def remove_cloud_alias(self, user_id, aliases):
        """Remove one or more cloud alias.

        Args:
            user_id (str/int): The user_id whose alias(es) need to be removed.
            aliases (str or list of str ): A single alias or multiple aliases in a list to be removed.
                e.g "x" or ["email@id", "y"]

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        if type(aliases) is str:
            aliases = [aliases]

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
            "cloudUsernames": aliases,
        }
        uri = u"{0}/{1}".format(self._uri_prefix, u"removecloudusernames")
        return self._session.post(uri, data=json.dumps(data))
