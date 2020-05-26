from py42.clients import BaseClient


class SavedSearchClient(BaseClient):
    """A client to interact with saved search APIs."""

    _version = u"v1"
    _resource = u"/forensic-search/queryservice/api/{}/saved".format(_version)

    _response_header = [u"name", u"id", u"notes", u"modifiedByUsername", u"modifiedTimestamp"]

    def __init__(self, session, file_event_client):
        super(SavedSearchClient, self).__init__(session)
        self._file_event_client = file_event_client

    def _parse_response(self, response):
        if u"searches" in response:
            return {
                key: search[key]
                for search in response[u"searches"]
                for key in self._response_header
            }

    def get(self):
        uri = u"{}".format(self._resource)
        response = self._session.get(uri)
        return self._parse_response(response)

    def get_by_id(self, search_id):
        uri = u"{}/{}".format(self._resource, search_id)
        return self._session.get(uri)

    def execute(self, search_id):
        response = self.get_by_id(search_id)
        if u"searches" in response:
            query = {}
            query[u"purpose"] = u"USER_EXECUTED_SEARCH"
            query[u"groups"] = response["searches"][0]["groups"]
            print(query)
            return self._file_event_client.search(query)
