from py42.clients import BaseClient


class SecurityClient(BaseClient):
    def get_security_event_locations(self, user_uid):
        uri = u"/c42api/v3/SecurityEventsLocation"
        params = {u"userUid": user_uid}
        return self._session.get(uri, params=params)


class SavedSearchClient(BaseClient):
    """A client to interact with saved search APIs."""

    _version = u"v1"
    _resource = u"/forensic-search/queryservice/api/{}/saved".format(_version)

    def __init__(self, session, file_event_client):
        super(SavedSearchClient, self).__init__(session)
        self._file_event_client = file_event_client

    def get(self):
        """Fetch details of existing saved searches.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"{}".format(self._resource)
        return self._session.get(uri)

    def get_by_id(self, search_id):
        """Fetch details of saved search for given search Id.

        Args:
            search_id (str): Unique search Id of the saved search, Required.
        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"{}/{}".format(self._resource, search_id)
        return self._session.get(uri)

    @staticmethod
    def _make_query(response):
        query = dict(pgNum=1, pgSize=100, purpose=u"USER_EXECUTED_SEARCH")
        query["groups"] = response[u"searches"][0][u"groups"]
        return query

    def execute(self, search_id):
        """
        Execute a saved search for given search Id and return incremental results based
        on the previous execution.

        Args:
            search_id (str): Unique search Id of the saved search, Required.
        Returns:
            :class:`py42.response.Py42Response`
        """
        response = self.get_by_id(search_id)
        query = SavedSearchClient._make_query(response)
        return self._file_event_client.search(query=query)
