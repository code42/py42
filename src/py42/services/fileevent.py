import json
from warnings import warn

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
        `REST Documentation <https://developer.code42.com/api/#operation/searchEventsUsingPOST>`__

        The existing data model for file events is deprecated.
        To use the updated data model for file events, `update your settings <https://py42docs.code42.com/en/stable/userguides/v2apis.html>`__.

        Args:
            query (:class:`~py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery` or str or unicode):
                A composed :class:`~py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery`
                object or the raw query as a JSON formatted string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the query results.
        """
        # if string query
        if isinstance(query, str):
            query = json.loads(query)
            # v2 fields are accessible via dot notation (exception of "@timestamp")
            version = "v2" if "." in query["srtKey"] or "@" in query["srtKey"] else "v1"
            uri = f"/forensic-search/queryservice/api/{version}/fileevent"
        # else query object
        else:
            # deprecation warning for v1 file events
            if query.version == "v1":
                warn(
                    "V1 file events are deprecated.  Use V2 queries instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )

            uri = f"/forensic-search/queryservice/api/{query.version}/fileevent"
            query = dict(query)

        try:
            return self._connection.post(uri, json=query)
        except Py42BadRequestError as err:
            if "INVALID_PAGE_TOKEN" in str(err.response.text):
                page_token = query.get("pgToken")
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
        uri = "/forensic-search/queryservice/api/v1/filelocations"
        return self._connection.get(uri, params={"sha256": checksum})
