from py42._internal.base_classes import BaseFileEventClient


class FileEventClient(BaseFileEventClient):

    def search_file_events(self, query, **kwargs):
        query = unicode(query)
        uri = "/forensic-search/queryservice/api/v1/fileevent"
        return self._session.post(uri, data=query, **kwargs)
