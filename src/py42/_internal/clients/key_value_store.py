from py42._internal.base_classes import BaseClient


class KeyValueStoreClient(BaseClient):
    def __init__(self, session):
        super(KeyValueStoreClient, self).__init__(session)

    def get_stored_value(self, key):
        uri = u"/v1/{0}".format(key)
        return self._default_session.get(uri)
