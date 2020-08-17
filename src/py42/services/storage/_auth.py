from py42.services._auth import C42RenewableAuth


class StorageTmpAuth(C42RenewableAuth):
    def __init__(self):
        super(StorageTmpAuth, self).__init__()
        self._cached_info = None

    def get_login_info(self):
        if self._cached_info is None:
            response = self.get_tmp_auth()
            self._cached_info = response
        return self._cached_info

    def clear_credentials(self):
        super(StorageTmpAuth, self).clear_credentials()

    def get_tmp_auth(self):
        raise NotImplementedError()

    def _get_credentials(self):
        if self._cached_info is None:
            self.get_login_info()
        login_token = self._cached_info[u"loginToken"]
        return u"{} {}".format(u"login_token", login_token)


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
        return u"{} {}-{}".format(u"token", response[0], response[1])
