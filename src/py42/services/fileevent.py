import json
from warnings import warn

from requests.adapters import HTTPAdapter
from urllib3 import Retry

import py42.settings.debug as debug
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InvalidPageTokenError
from py42.services import BaseService


class FFSQueryRetryStrategy(Retry):
    """The forensic search service helpfully responds with a 'retry-after' header, telling us how long until the rate
    limiter is reset. We subclass :class:`urllib3.Retry` just to add a bit of logging so the user can tell why the
    request might look like it's hanging.
    """

    def get_retry_after(self, response):
        retry_after = super().get_retry_after(response)
        if retry_after is not None:
            debug.logger.info(
                f"Forensic search rate limit hit, retrying after: {int(retry_after)} seconds."
            )
        return retry_after

    def get_backoff_time(self):
        backoff_time = super().get_backoff_time()
        debug.logger.info(
            f"Forensic search rate limit hit, retrying after: {backoff_time} seconds."
        )
        return backoff_time


class FileEventService(BaseService):
    """A service for searching file events.

    See the :ref:`Executing Searches User Guide <anchor_search_file_events>` to learn more about how
    to construct a query.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._retry_adapter_mounted = False

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
        self._mount_retry_adapter()

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
        self._mount_retry_adapter()

        uri = "/forensic-search/queryservice/api/v1/filelocations"
        return self._connection.get(uri, params={"sha256": checksum})

    def _mount_retry_adapter(self):
        """Sets custom Retry strategy for FFS url requests to gracefully handle being rate-limited on FFS queries."""
        if not self._retry_adapter_mounted:
            retry_strategy = FFSQueryRetryStrategy(
                status=3,  # retry up to 3 times
                backoff_factor=5,  # if `retry-after` header isn't present, use 5 second exponential backoff
                allowed_methods=[
                    "POST"
                ],  # POST isn't a default allowed method due to it usually modifying resources
                status_forcelist=[
                    429
                ],  # this only handles 429 errors, it won't retry on 5xx
            )
            file_event_adapter = HTTPAdapter(
                pool_connections=200,
                pool_maxsize=4,
                pool_block=True,
                max_retries=retry_strategy,
            )
            self._connection._session.mount(
                self._connection.host_address, file_event_adapter
            )
            self._retry_adapter_mounted = True
