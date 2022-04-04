import json

import py42.settings as settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42Error
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

        The existing data model for file events will be DEPRECATED in late spring 2023. TODO: placeholder
        To use the updated data model for file events, update your settings<https://developer.code42.com>.

        Args:
            query (:class:`~py42.sdk.queries.fileevents.file_event_query.FileEventQuery` or str or unicode):
                A composed :class:`~py42.sdk.queries.fileevents.file_event_query.FileEventQuery`
                object or the raw query as a JSON formatted string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the query results.
        """

        # check if query type matches settings
        if not isinstance(query, str):
            if query.sort_key == "eventId" and settings.use_v2_file_event_data:
                raise Py42Error(
                    "Bad Request. You cannot use a V1 query with V2 settings enabled. For more details on working with V2 file event data, see the 'V2 File Events' user guide at https://py42docs.code42.com/."
                )
            elif query.sort_key == "event.id" and not settings.use_v2_file_event_data:
                raise Py42Error(
                    "Bad Request. You cannot use a V2 query with V2 settings disabled. For more details on working with V2 file event data, see the 'V2 File Events' user guide at https://py42docs.code42.com/."
                )

        version = "v2" if settings.use_v2_file_event_data else "v1"
        uri = f"/forensic-search/queryservice/api/{version}/fileevent"

        if isinstance(query, str):
            query = json.loads(query)
        else:
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

        # TODO: unknown status as of 4-4-22

        Args:
            checksum (str): SHA256 checksum of a file.

        Returns:
            :class:`py42.response.Py42Response`: A response containing file details.
        """
        uri = "/forensic-search/queryservice/api/v1/filelocations"
        return self._connection.get(uri, params={"sha256": checksum})
