from py42.services import BaseService


class KeyValueStoreService(BaseService):
    def __init__(self, connection):
        super().__init__(connection)

    def get_stored_value(self, key):
        uri = f"/v1/{key}"
        # this request doesn't expect json, unlike most.
        headers = {"Accept": "*/*"}
        return self._connection.get(uri, headers=headers)
