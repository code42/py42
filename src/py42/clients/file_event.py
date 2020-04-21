from py42._internal.compat import str
from py42.clients import BaseClient


class FileEventClient(BaseClient):
    """A client for searching file events.

    See the :ref:`Executing Searches User Guide <anchor_search_file_events>` to learn more about how
    to construct a query.
    """

    def search(self, query):
        """Searches for file events matching the query criteria.
        `REST Documentation <https://forensicsearch-east.us.code42.com/forensic-search/queryservice/swagger-ui.html#/file-event-controller/searchEventsUsingPOST>`__

        Args:
            query (:class:`FileEventQuery` or str): A composed FileEventQuery object or the raw
                query as a JSON formatted string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the query results.
        """
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return self._session.post(uri, data=query)
