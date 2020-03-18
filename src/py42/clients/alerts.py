import json

from py42._internal.compat import str
from py42.clients import BaseClient


class AlertClient(BaseClient):
    """A client for interacting with Code42 security alerts.

    The AlertClient has the ability to search, resolve, and reopen alerts.
    Also, it can get the details for the file event query for the event that triggered the alert.
    """

    _uri_prefix = u"/svc/api/v1/{0}"

    def __init__(self, session, user_context):
        super(AlertClient, self).__init__(session)
        self._user_context = user_context

    def search(self, query):
        """Searches alerts using the given :class:`py42.sdk.queries.alerts.alert_query.AlertQuery`.

        Args:
            query (:class:`py42.sdk.queries.alerts.alert_query.AlertQuery`): An alert query.
                See `userguides.searches` to learn more about how to construct a query.

        Returns:
            :class:`py42.sdk.response`: A response containing the alerts that match the given query.
        """
        query = str(query)
        uri = self._uri_prefix.format(u"query-alerts")
        return self._session.post(uri, data=query)

    def get_query_details(self, alert_ids, tenant_id=None):
        """Gets the details for a file event query that when passed into a search would result in
        events that could be responsible for the alerts with the given alert IDs.

        Args:
            alert_ids (iter[str]): The alert IDs for the alerts to get file event query details for.
            tenant_id (str): The tenant ID for the tenant that the alerts belong to. When given None,
                it uses the currently logged in user's tenant ID. Defaults to None.

        Returns:
            :class:`py42.sdk.response`:  A response containing file event query details.
        """
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        return self._session.post(uri, data=json.dumps(data))

    def resolve(self, alert_ids, tenant_id=None, reason=None):
        """Resolves the alerts with the given alert IDs.

        Args:
            alert_ids (iter[str]): The alert IDs for the alerts to resolve.
            tenant_id (str, optional): The tenant ID for the tenant that the alerts belong to.
                When given None, it uses the currently logged in user's tenant ID. Defaults to None.
            reason (str, optional): The reason the alerts are now resolved.

        Returns:
            :class:`py42.sdk.response`
        """
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        reason = reason if reason else u""
        uri = self._uri_prefix.format(u"resolve-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))

    def reopen(self, alert_ids, tenant_id=None, reason=None):
        """Reopens the resolved alerts with the given alert IDs.

        Args:
            alert_ids (iter[str]): The alert IDs for the alerts to reopen.
            tenant_id (str): The tenant ID for the tenant that the alerts belong to. When given None,
                it uses the currently logged in user's tenant ID. Defaults to None.
            reason (str): The reason the alerts are reopened.

        Returns:
            :class:`py42.sdk.response`
        """
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"reopen-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))
