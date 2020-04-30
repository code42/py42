import json

from py42._internal.compat import str
from py42.clients import BaseClient
from py42.clients.util import get_all_pages


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
                See the :ref:`Executing Searches User Guide <anchor_search_alerts>` to learn more
                about how to construct a query.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the alerts that match the given
            query.
        """
        query = self._add_tenant_id_if_missing(query)
        uri = self._uri_prefix.format(u"query-alerts")
        return self._session.post(uri, data=query)

    def get_details(self, alert_ids, tenant_id=None):
        """Gets the details for the alerts with the given IDs, including the file event query that,
        when passed into a search, would result in events that could have triggered the alerts.

        Args:
            alert_ids (iter[str]): The identification numbers of the alerts for which you want to
                get details for.
            tenant_id (str, optional): The unique identifier of the tenant that the alerts belong to.
                When given None, it uses the currently logged in user's tenant ID. Defaults to
                None.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the alert details.
        """
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        return self._session.post(uri, data=json.dumps(data))

    def resolve(self, alert_ids, tenant_id=None, reason=None):
        """Resolves the alerts with the given IDs.

        Args:
            alert_ids (iter[str]): The identification numbers for the alerts to resolve.
            tenant_id (str, optional): The unique identifier for the tenant that the alerts belong
                to. When given None, it uses the currently logged in user's tenant ID. Defaults to
                None.
            reason (str, optional): The reason the alerts are now resolved. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        reason = reason if reason else u""
        uri = self._uri_prefix.format(u"resolve-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))

    def reopen(self, alert_ids, tenant_id=None, reason=None):
        """Reopens the resolved alerts with the given IDs.

        Args:
            alert_ids (iter[str]): The identification numbers for the alerts to reopen.
            tenant_id (str, optional): The unique identifier for the tenant that the alerts belong
                to. When given None, it uses the currently logged in user's tenant ID. Defaults to
                None.
            reason (str, optional): The reason the alerts are reopened. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"reopen-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))

    def _add_tenant_id_if_missing(self, query):
        query_dict = json.loads(str(query))
        tenant_id = query_dict.get(u"tenantId", None)
        if tenant_id is None:
            query_dict[u"tenantId"] = self._user_context.get_current_tenant_id()
            return json.dumps(query_dict)
        else:
            return str(query)

    def _get_alert_rules(
        self, tenant_id, sort_key=None, sort_direction=None, page_num=None, page_size=None
    ):
        data = {
            "tenantId": tenant_id,
            "groups": [],
            "groupClause": "AND",
            "pgNum": page_num - 1,  # Minus 1, as this API expects first page to start with zero.
            "pgSize": page_size,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        uri = self._uri_prefix.format(u"rules/query-rule-metadata")
        return self._session.post(uri, data=json.dumps(data))

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str): Sort results based by field. Defaults to 'CreatedAt'.
            sort_direction (str): ``ASC`` or ``DESC``. Defaults to "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
        """
        tenant_id = self._user_context.get_current_tenant_id()
        return get_all_pages(
            self._get_alert_rules,
            u"ruleMetadata",
            tenant_id=tenant_id,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_rules_by_name(self, rule_name):
        """Fetch a rule by its name.

        Args:
            rule_name (str): Rule name to search for, case insensitive search.

        Returns
            :list: List of dictionary containing rule-details.
        """
        rule_pages = self.get_all()
        matched_rules = []
        for rule_page in rule_pages:
            rules = rule_page["ruleMetadata"]
            for rule in rules:
                if rule_name.lower() in rule["name"].lower():
                    matched_rules.append(rule)
        return matched_rules
