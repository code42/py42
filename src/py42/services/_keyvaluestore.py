from py42.services import BaseService


class KeyValueStoreService(BaseService):
    def __init__(self, connection):
        super(KeyValueStoreService, self).__init__(connection)

    def get_stored_value(self, key):
        uri = u"/v1/{}".format(key)
        # this request doesn't expect json, unlike most.
        headers = {u"Accept": u"*/*"}
        return self._connection.get(uri, headers=headers)
