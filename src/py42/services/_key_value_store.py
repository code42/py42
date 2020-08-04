from py42.services import BaseClient


class KeyValueStoreClient(BaseClient):
    def __init__(self, cnxn):
        super(KeyValueStoreClient, self).__init__(cnxn)

    def get_stored_value(self, key):
        uri = u"/v1/{}".format(key)
        return self._connection.get(uri)
