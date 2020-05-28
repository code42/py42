import json

from py42.clients import BaseClient
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery


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
        """Fetch the details of a saved search by its given search Id.

        Args:
            search_id (str): Unique search Id of the saved search.
        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"{}/{}".format(self._resource, search_id)
        return self._session.get(uri)

    def execute(self, search_id, pg_num=1, pg_size=10000):
        """
        Execute a saved search for given search Id and return its results.

        Args:
            search_id (str): Unique search Id of the saved search.
            pg_num (int): The consecutive group of results of size pg_size in the result set to return.
            pg_size (int): The maximum number of results to be returned.
        Returns:
            :class:`py42.response.Py42Response`
        """
        response = self.get_by_id(search_id)
        search = response[u"searches"][0]
        print(search)
        query = FileEventQuery.from_dict(search)
        print(str(query))
        return self._file_event_client.search(query)
