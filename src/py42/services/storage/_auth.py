from py42.services._auth import C42RenewableAuth


class StorageTmpAuth(C42RenewableAuth):
    def __init__(self):
        super(StorageTmpAuth, self).__init__()
        self._storage_url = None

    def get_storage_url(self):
        self.get_credentials()
        return self._server_url

    def get_tmp_auth(self):
        raise NotImplementedError()

    def _get_credentials(self):
        login_info = self.get_tmp_auth()
        login_token = login_info[u"loginToken"]
        self._server_url = login_info[u"serverUrl"]
        return u"login_token {}".format(login_token)


class FileArchiveTmpAuth(StorageTmpAuth):
    def __init__(self, connection, user_id, device_guid, destination_guid):
        super(FileArchiveTmpAuth, self).__init__()
        self._connection = connection
        self._user_id = user_id
        self._device_guid = device_guid
        self._destination_guid = destination_guid

    def get_tmp_auth(self):
        uri = u"/api/LoginToken"
        data = {
            u"userId": self._user_id,
            u"sourceGuid": self._device_guid,
            u"destinationGuid": self._destination_guid,
        }
        response = self._connection.post(uri, json=data)
        return response


class SecurityArchiveTmpAuth(StorageTmpAuth):
    def __init__(self, connection, plan_uid, destination_guid):
        super(SecurityArchiveTmpAuth, self).__init__()
        self._connection = connection
        self._plan_uid = plan_uid
        self._destination_guid = destination_guid

    def get_tmp_auth(self):
        uri = u"/api/StorageAuthToken"
        data = {u"planUid": self._plan_uid, u"destinationGuid": self._destination_guid}
        response = self._connection.post(uri, json=data)
        return response


class V1Auth(C42RenewableAuth):
    def __init__(self, storage_tmp_session):
        super(V1Auth, self).__init__()
        self._auth_session = storage_tmp_session

    def _get_credentials(self):
        uri = u"/api/AuthToken"
        response = self._auth_session.post(uri)
        return u"token {}-{}".format(response[0], response[1])
