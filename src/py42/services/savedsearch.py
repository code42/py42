from py42.services.util import escape_quote_chars
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.services import BaseService


class SavedSearchService(BaseService):
    """A service to interact with saved search APIs."""

    _version = "v1"
    _resource = f"/forensic-search/queryservice/api/{_version}/saved"

    def __init__(self, connection, file_event_client):
        super().__init__(connection)
        self._file_event_client = file_event_client

    def get(self):
        """Fetch details of existing saved searches.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"{self._resource}"
        return self._connection.get(uri)

    def get_by_id(self, search_id):
        """Fetch the details of a saved search by its given search Id.

        Args:
            search_id (str): Unique search Id of the saved search.
        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"{self._resource}/{search_id}"
        return self._connection.get(uri)

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
        return self._file_event_client.search(query)

    def execute_get_all(self, search_id, page_token=''):
        """
        Executes a saved search for given search Id, returns a page of events with a token in the response to retrieve next page.

        Args:
            search_id (str): Unique search Id of the saved search.
            page_token (str, optional): A token used to indicate the starting point for
                additional page results. For the first page, do not pass ``page_token``. For
                all consecutive pages, pass the token from the previous response from
                field ``nextPgToken``. Defaults to empty string.
        Returns:
            :class:`py42.response.Py42Response`: A response containing a page of events.
        """
        query = self.get_query(search_id)
        query.page_token = escape_quote_chars(page_token)
        return self._file_event_client.search(query)
