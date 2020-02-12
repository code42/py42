from py42._internal.base_classes import BaseClient
from py42._internal.compat import str


class FileEventClient(BaseClient):
    def search_file_events(self, query):
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return self._default_session.post(uri, data=query)
