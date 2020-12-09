from py42._compat import str
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InvalidPageTokenError
from py42.services import BaseService


class FileEventService(BaseService):
    """A service for searching file events.

    See the :ref:`Executing Searches User Guide <anchor_search_file_events>` to learn more about how
    to construct a query.
    """

    def search(self, query):
        """Searches for file events matching the query criteria.
        `REST Documentation <https://forensicsearch-east.us.code42.com/forensic-search/queryservice/swagger-ui.html#/file-event-controller/searchEventsUsingPOST>`__

        Args:
            query (:class:`~py42.sdk.queries.fileevents.file_event_query.FileEventQuery` or str):
                A composed :class:`~py42.sdk.queries.fileevents.file_event_query.FileEventQuery`
                object or the raw query as a JSON formatted string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the query results.
        """
        try:
            query_str = str(query)
            uri = u"/forensic-search/queryservice/api/v1/fileevent"
            return self._connection.post(uri, data=query_str)
        except Py42BadRequestError as err:
            if u"INVALID_PAGE_TOKEN" in str(err.response.text):
                page_token = query.page_token
                if page_token:
                    raise Py42InvalidPageTokenError(err, page_token)
            raise

    def get_file_location_detail_by_sha256(self, checksum):
        """Get file location details based on SHA256 hash.

        Args:
            checksum (str): SHA256 checksum of a file.

        Returns:
            :class:`py42.response.Py42Response`: A response containing file details.
        """
        uri = u"/forensic-search/queryservice/api/v1/filelocations"
        return self._connection.get(uri, params={u"sha256": checksum})
