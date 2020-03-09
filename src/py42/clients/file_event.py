from py42.clients import BaseClient
from py42._internal.compat import str
from py42.sdk.response import Py42Response


class FileEventClient(BaseClient):
    def search(self, query):
        query = str(query)
        uri = u"/forensic-search/queryservice/api/v1/fileevent"
        return Py42Response(self._session.post(uri, data=query), json_key=u"fileEvents")
