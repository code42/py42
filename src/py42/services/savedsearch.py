from warnings import warn

import py42.settings as settings
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.services import BaseService


class SavedSearchService(BaseService):
    """A service to interact with saved search APIs."""

    def __init__(self, connection, file_event_service):
        super().__init__(connection)
        self._file_event_service = file_event_service
        self._uri = ""

    @property
    def uri(self):
        # construct uri every call to see if settings changed
        _version = "v2" if settings.use_v2_file_event_data else "v1"
        self._uri = f"/forensic-search/queryservice/api/{_version}/saved"
        return self._uri

    def get(self):
        """Fetch details of existing saved searches.

        The existing data model for file events and saved searches is deprecated.
        To use the updated data model for file events, `update your settings <https://py42docs.code42.com/en/stable/userguides/v2apis.html>`__.
        Retrieving saved searches with V2 settings enabled will convert existing saved search queries to the V2 data model.  Existing V1 queries that cannot be properly converted will be excluded from the response.


        Returns:
            :class:`py42.response.Py42Response`
        """

        # deprecation warning for v1 file events
        if not settings.use_v2_file_event_data:
            warn(
                "V1 file events and saved searches are deprecated.  Set 'py42.settings.use_v2_file_event_data = True' to use V2 file events.",
                DeprecationWarning,
                stacklevel=2,
            )

        print(self.uri)
        return self._connection.get(self.uri)

    def get_by_id(self, search_id):
        """Fetch the details of a saved search by its given search Id.

        The existing data model for file events and saved searches is deprecated.
        To use the updated data model for file events, `update your settings <https://py42docs.code42.com/en/stable/userguides/v2apis.html>`__.
        Retrieving saved searches with V2 settings enabled will convert existing saved search queries to the V2 data model.  Existing V1 queries that cannot be properly converted will be excluded from the response.

        Args:
            search_id (str): Unique search Id of the saved search.
        Returns:
            :class:`py42.response.Py42Response`
        """

        # deprecation warning for v1 file events
        if not settings.use_v2_file_event_data:
            warn(
                "V1 file events and saved searches are deprecated.  Set 'py42.settings.use_v2_file_event_data = True' to use V2 file events.",
                DeprecationWarning,
                stacklevel=2,
            )

        return self._connection.get(f"{self.uri}/{search_id}")

    def get_query(self, search_id, page_number=None, page_size=None):
        """Get the saved search in form of a query(`py42.sdk.queries.fileevents.file_event_query`).

        Args:
            search_id (str): Unique search Id of the saved search.
            page_number (int, optional): The consecutive group of results of size page_size in the result set to return. Defaults to None.
            page_size (int, optional): The maximum number of results to be returned. Defaults to None.
        Returns:
            :class:`py42.sdk.queries.fileevents.file_event_query.FileEventQuery`
        """

        response = self.get_by_id(search_id)
        search = response["searches"][0]
        return FileEventQuery.from_dict(
            search, page_number=page_number, page_size=page_size
        )

    def execute(self, search_id, page_number=None, page_size=None):
        """
        Executes a saved search for given search Id, returns up to the first 10,000 events.

        Args:
            search_id (str): Unique search Id of the saved search.
            page_number (int, optional): The consecutive group of results of size page_size in the result set to return. Defaults to None.
            page_size (int, optional): The maximum number of results to be returned. Defaults to None.
        Returns:
            :class:`py42.response.Py42Response`
        """
        query = self.get_query(search_id, page_number=page_number, page_size=page_size)
        return self._file_event_service.search(query)

    def search_file_events(self, search_id, page_number=None, page_size=None):
        """
        Alias method for :meth:`~execute()`. Executes a saved search for given search Id, returns up to the first 10,000 events.

        To view more than the first 10,000 events:
            * pass the :data:`search_id` to :meth:`~get_query()`
            * pass the resulting query (:class:`~py42.sdk.queries.fileevents.file_event_query.FileEventQuery`) to :meth:`~py42.clients.securitydata.SecurityDataClient.search_all_file_events()`, use that method as normal.

        Args:
            search_id (str): Unique search Id of the saved search.
            page_number (int, optional): The consecutive group of results of size page_size in the result set to return. Defaults to None.
            page_size (int, optional): The maximum number of results to be returned. Defaults to None.
        Returns:
            :class:`py42.response.Py42Response`
        """
        return self.execute(search_id, page_number=page_number, page_size=page_size)
