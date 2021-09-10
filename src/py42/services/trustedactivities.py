from py42.services import BaseService


class TrustedActivitiesService(BaseService):

    _uri_prefix = "/api/v1/trusted-activities"

    def __init__(self, connection):
        super().__init__(connection)

    def get_all(self, type):
        params = {"type": type}
        return self._connection.get(self._uri_prefix, params=params)

    def create(
        self, type, value, description
    ):  # change this name probably, these should all be strings
        data = {
            "type": type,
            "value": value,
            "description": description,
        }
        return self._connection.post(self._uri_prefix, json=data)

    def get(self, id):  # id should be int
        uri = f"{self._uri_prefix}/{id}"
        return self._connection.get(uri)

    def update(self, id, type, value, description):
        uri = f"{self._uri_prefix}/{id}"
        data = {
            "type": type,
            "value": value,
            "description": description,
        }
        return self._connection.post(uri, json=data)

    def delete(self, id):
        uri = f"{self._uri_prefix}/{id}"
        return self._connection.delete(uri)
