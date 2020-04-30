class AlertRulesModule(object):
    def __init__(self, microservice_client_factory, user_client):
        self.microservice_client_factory = microservice_client_factory
        self._user_client = user_client
        self._alert_client = None

    @property
    def rules(self):
        return self.microservice_client_factory.get_alert_rules_client(
            self.microservice_client_factory.get_detection_list_user_client(self._user_client)
        )

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str): Sort results based by field. Defaults to 'CreatedAt'.
            sort_direction (str): ``ASC`` or ``DESC``. Defaults to  "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
        """
        alert_client = self.microservice_client_factory.get_alerts_client()
        return alert_client.get_all(sort_key=sort_key, sort_direction=sort_direction)

    def get_by_name(self, rule_name):
        """Fetch a rule by its name.

        Args:
            rule_name (str): Rule name to search for, case insensitive search.

        Returns
            :dict: Dictionary containing rule-details.
        """
        alert_client = self.microservice_client_factory.get_alerts_client()
        return alert_client.get_rules_by_name(rule_name)
