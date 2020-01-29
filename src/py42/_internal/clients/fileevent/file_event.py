from py42._internal.base_classes import BaseFileEventClient
from py42._internal.compat import str


class FileEventClient(BaseFileEventClient):
    def search_file_events(self, query):
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return self._session.post(uri, data=query)
