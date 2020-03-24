from py42._internal.compat import str
from py42.clients import BaseClient


class FileEventClient(BaseClient):
    """A client for interacting with Code42 Forensic File Search events.
    """

    def search(self, query):
        """Searches for file events matching query criteria.

        Args:
            query ():
        """
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return self._session.post(uri, data=query)
