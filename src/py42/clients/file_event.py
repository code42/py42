from py42._internal.compat import str
from py42.clients import BaseClient


class FileEventClient(BaseClient):
    def search(self, query):
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return self._session.post(uri, data=query)
