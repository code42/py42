from py42.sdk.queries.alerts.filters import AlertState


class AlertsClient:
    """A client to expose alert API.

    `Rest Documentation <https://developer.code42.com/api/#tag/Alerts>`__
    """

    def __init__(self, alert_service, alert_rules_client):
        self._alert_service = alert_service
        self._alert_rules_client = alert_rules_client

    @property
    def rules(self):
        """A collection of methods for managing alert rules.

        Returns:
            :class:`py42.services.alertrules.AlertRulesClient`
        """
        return self._alert_rules_client

    def search(self, query, page_num=1, page_size=None):
        """Searches alerts using the given :class:`py42.sdk.queries.alerts.alert_query.AlertQuery`.

        `Rest Documentation <https://developer.code42.com/api/#operation/Alerts_QueryAlert>`__

        Args:
            query (:class:`py42.sdk.queries.alerts.alert_query.AlertQuery`): An alert query.
                See the :ref:`Executing Searches User Guide <anchor_search_alerts>` to learn more
                about how to construct a query.
            page_num (int, optional): The page number to get. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to `py42.settings.items_per_page`.


        Returns:
            :class:`py42.response.Py42Response`: A response containing the alerts that match the given
            query.
        """
        return self._alert_service.search(query, page_num, page_size)

    def search_all_pages(self, query):
        """Searches alerts using the given :class:`py42.sdk.queries.alerts.alert_query.AlertQuery`.

        `Rest Documentation <https://developer.code42.com/api/#operation/Alerts_QueryAlert>`__

        Args:
            query (:class:`py42.sdk.queries.alerts.alert_query.AlertQuery`): An alert query.
                See the :ref:`Executing Searches User Guide <anchor_search_alerts>` to learn more
                about how to construct a query.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of alerts that match the given query.
        """
        return self._alert_service.search_all_pages(query)

    def get_details(self, alert_ids):
        """Gets the details for the alerts with the given IDs, including the file event query that,
        when passed into a search, would result in events that could have triggered the alerts.

        `Rest Documentation <https://developer.code42.com/api/#operation/Alerts_QueryAlertDetails>`__

        Args:
            alert_ids (str or list[str]): The identification number(s) of the alerts for which you want to
                get details for. Note: The alerts backend accepts a maximum of 100 alerts per request.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the alert details.
        """
        return self._alert_service.get_details(alert_ids)

    def resolve(self, alert_ids, reason=None):
        """Resolves the alerts with the given IDs.

        Args:
            alert_ids (str or list[str]): The identification number(s) for the alerts to resolve.
                Note: The alerts backend accepts a maximum of 100 alerts per request.
            reason (str, optional): The reason the alerts are now resolved. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._alert_service.update_state(
            AlertState.DISMISSED, alert_ids, note=reason
        )

    def reopen(self, alert_ids, reason=None):
        """Reopens the resolved alerts with the given IDs.

        Args:
            alert_ids (str or list[str]): The identification number(s) for the alerts to reopen.
                Note: The alerts backend accepts a maximum of 100 alerts per request.
            reason (str, optional): The reason the alerts are reopened. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._alert_service.update_state(AlertState.OPEN, alert_ids, note=reason)

    def update_state(self, status, alert_ids, note=None):
        """Updates the status of alerts.

        Args:
            status (str): Status to set from OPEN, RESOLVED, PENDING, IN_PROGRESS
            alert_ids (str or list[str]): The identification number(s) for the alerts to reopen.
                Note: The alerts backend accepts a maximum of 100 alerts per request.
            note (str, optional): A note to attach to the alerts. Must be less than 2000
                characters. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._alert_service.update_state(status, alert_ids, note=note)

    def update_note(self, alert_id, note):
        """Updates an alert's note.

        Args:
            alert_id (str): The identification number of an alert to add a note to.
            note (str): A note to attach to the alert. Must be less than 2000
                characters. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._alert_service.update_note(alert_id, note)

    def get_aggregate_data(self, alert_id):
        """Gets alert summary with details about observations.

        Args:
            alert_id (str): Gets the details for the alert with the given ID.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._alert_service.get_aggregate_data(alert_id)

    def get_all_alert_details(self, query):
        """
        Helper method that combines :func:`.search_all_pages()` and :func:`.get_details()`
        methods to get alert objects with alert "observations" details populated.
        Returns an iterator of alert detail objects.

        Note: automatically overrides the `page_size` property on the query object to limit
        search to 100 results per page, as that is the max that :func:`.get_details()` can
        request at a time.

        Args:
            query (:class:`py42.sdk.queries.alerts.alert_query.AlertQuery`): An alert query.

        Returns:
            generator: An object that iterates over alert detail items.
        """
        query.page_size = 25
        sort_key = query.sort_key[0].lower() + query.sort_key[1:]
        if sort_key == "alertId":
            sort_key = "id"
        reverse = query.sort_direction == "desc"
        pages = self._alert_service.search_all_pages(query)
        for page in pages:
            alert_ids = [alert["id"] for alert in page["alerts"]]
            if alert_ids:
                alert_details = self._alert_service.get_details(alert_ids)
                yield from sorted(
                    alert_details["alerts"],
                    key=lambda x: x.get(sort_key),
                    reverse=reverse,
                )
            else:
                yield from []
