from py42.modules.alertrules import AlertRulesModule


class AlertsModule(object):
    def __init__(self, microservice_client_factory, user_client, alert_rules_module=None):
        self._microservice_client_factory = microservice_client_factory
        self._alert_rules_module = AlertRulesModule(self._microservice_client_factory, user_client)

    @property
    def rules(self):
        return self._alert_rules_module

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
        alert_client = self._microservice_client_factory.get_alerts_client()

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
        alert_client = self._microservice_client_factory.get_alerts_client()

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
        alert_client = self._microservice_client_factory.get_alerts_client()

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
        alert_client = self._microservice_client_factory.get_alerts_client()

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str): Sort results based by field. Defaults to 'CreatedAt'.
            sort_direction (str): ``ASC`` or ``DESC``. Defaults to "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
        """
        alert_client = self._microservice_client_factory.get_alerts_client()

    def get_rules_by_name(self, rule_name):
        """Fetch a rule by its name.

        Args:
            rule_name (str): Rule name to search for, case insensitive search.

        Returns
            :list: List of dictionary containing rule-details.
        """
        pass
