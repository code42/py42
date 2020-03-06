from py42._internal.base_classes import BaseClient
from py42._internal.compat import str
from py42._internal.response import Py42Response


class FileEventClient(BaseClient):
    def search(self, query):
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return Py42Response(self._session.post(uri, data=query))
