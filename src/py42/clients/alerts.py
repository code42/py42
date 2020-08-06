class AlertsClient(object):
    def __init__(self, alert_service, alert_rules_client):
        self._alert_service = alert_service
        self._alert_rules_client = alert_rules_client

    @property
    def rules(self):
        """A collection of methods for managing alert rules.

        Returns:
            :class:`py42.clients.alertrules.AlertRulesClient`
        """
        return self._alert_rules_client

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
        return self._alert_service.search(query)

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
        return self._alert_service.get_details(alert_ids, tenant_id=tenant_id)

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
        return self._alert_service.resolve(
            alert_ids, tenant_id=tenant_id, reason=reason
        )

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
        return self._alert_service.reopen(alert_ids, tenant_id=tenant_id, reason=reason)