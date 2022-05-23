from warnings import warn

from py42.sdk.queries.fileevents.file_event_query import (
    FileEventQuery as FileEventQueryV1,
)
from py42.sdk.queries.fileevents.v2.file_event_query import (
    FileEventQuery as FileEventQueryV2,
)
from py42.services import BaseService


class SavedSearchService(BaseService):
    """A service to interact with saved search APIs."""

    def __init__(self, connection, file_event_service):
        super().__init__(connection)
        self._file_event_service = file_event_service
        self._uri = ""
        self._version = "v1"

    @property
    def uri(self):
        # construct uri every call to see if settings changed
        self._uri = f"/forensic-search/queryservice/api/{self._version}/saved"
        return self._uri

    def get(self, use_v2=False):
        """Fetch details of existing saved searches.

        The existing data model for file events and saved searches is deprecated.
        To use the updated data model for file events, `update your settings <https://py42docs.code42.com/en/stable/userguides/v2apis.html>`__.
        Retrieving saved searches with V2 settings enabled will convert existing saved search queries to the V2 data model.  Existing V1 queries that cannot be properly converted will be excluded from the response.

        Args:
            use_v2 (bool): Flag to use v2 file events and saved searches. Defaults to False.
        Returns:
            :class:`py42.response.Py42Response`
        """

        # deprecation warning for v1 file events
        if not use_v2:
            warn(
                "V1 file events and saved searches are deprecated.  Use v2 apis by passing in the optional use_v2=True arg.",
                DeprecationWarning,
                stacklevel=2,
            )

        self._version = "v2" if use_v2 else "v1"
        return self._connection.get(self.uri)

    def get_by_id(self, search_id, use_v2=False):
        """Fetch the details of a saved search by its given search Id.

        The existing data model for file events and saved searches is deprecated.
        To use the updated data model for file events, `update your settings <https://py42docs.code42.com/en/stable/userguides/v2apis.html>`__.
        Retrieving saved searches with V2 settings enabled will convert existing saved search queries to the V2 data model.  Existing V1 queries that cannot be properly converted will be excluded from the response.

        Args:
            search_id (str): Unique search Id of the saved search.
            use_v2 (bool): Flag to use v2 file events and saved searches. Defaults to False.
        Returns:
            :class:`py42.response.Py42Response`
        """

        # deprecation warning for v1 file events
        if not use_v2:
            warn(
                "V1 file events and saved searches are deprecated.  Use v2 apis by passing in the optional use_v2=True arg.",
                DeprecationWarning,
                stacklevel=2,
            )
        self._version = "v2" if use_v2 else "v1"
        return self._connection.get(f"{self.uri}/{search_id}")

    def get_query(self, search_id, page_number=None, page_size=None, use_v2=False):
        """Get the saved search in form of a query(`py42.sdk.queries.fileevents.file_event_query`).

        Args:
            search_id (str): Unique search Id of the saved search.
            page_number (int, optional): The consecutive group of results of size page_size in the result set to return. Defaults to None.
            page_size (int, optional): The maximum number of results to be returned. Defaults to None.
            use_v2 (bool): Flag to use v2 file events and saved searches. Defaults to False.
        Returns:
            :class:`py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery`
        """

        response = self.get_by_id(search_id, use_v2=use_v2)
        search = response["searches"][0]
        if use_v2:
            return FileEventQueryV2.from_dict(
                search, page_number=page_number, page_size=page_size
            )
        return FileEventQueryV1.from_dict(
            search, page_number=page_number, page_size=page_size
        )

    def execute(self, search_id, page_number=None, page_size=None, use_v2=False):
        """
        Executes a saved search for given search Id, returns up to the first 10,000 events.

        Args:
            search_id (str): Unique search Id of the saved search.
            page_number (int, optional): The consecutive group of results of size page_size in the result set to return. Defaults to None.
            page_size (int, optional): The maximum number of results to be returned. Defaults to None.
            use_v2 (bool): Flag to use v2 file events and saved searches. Defaults to False.
        Returns:
            :class:`py42.response.Py42Response`
        """
        query = self.get_query(
            search_id, page_number=page_number, page_size=page_size, use_v2=use_v2
        )
        return self._file_event_service.search(query)

    def search_file_events(
        self, search_id, page_number=None, page_size=None, use_v2=False
    ):
        """
        Alias method for :meth:`~execute()`. Executes a saved search for given search Id, returns up to the first 10,000 events.

        To view more than the first 10,000 events:
            * pass the :data:`search_id` to :meth:`~get_query()`
            * pass the resulting query (:class:`~py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery`) to :meth:`~py42.clients.securitydata.SecurityDataClient.search_all_file_events()`, use that method as normal.

        Args:
            search_id (str): Unique search Id of the saved search.
            page_number (int, optional): The consecutive group of results of size page_size in the result set to return. Defaults to None.
            page_size (int, optional): The maximum number of results to be returned. Defaults to None.
            use_v2 (bool): Flag to use v2 file events and saved searches. Defaults to False.
        Returns:
            :class:`py42.response.Py42Response`
        """
        return self.execute(
            search_id, page_number=page_number, page_size=page_size, use_v2=use_v2
        )
