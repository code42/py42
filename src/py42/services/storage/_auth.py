import json

from py42.services._auth import C42RenewableAuth


class StorageTmpAuth(C42RenewableAuth):
    def __init__(self):
        super(StorageTmpAuth, self).__init__()
        self._cached_info = None

    def get_login_info(self):
        if self._cached_info is None:
            response = self.get_tmp_auth_token()
            self._cached_info = response
        return self._cached_info

    def clear_credentials(self):
        self._cached_info = None
        super(StorageTmpAuth, self).clear_credentials()

    def get_tmp_auth_token(self):
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

    def get_tmp_auth_token(self):
        uri = u"/api/LoginToken"
        data = {
            u"userId": self._user_id,
            u"sourceGuid": self._device_guid,
            u"destinationGuid": self._destination_guid,
        }
        response = self._connection.post(uri, data=json.dumps(data))
        return response


class SecurityArchiveTmpAuth(StorageTmpAuth):
    def __init__(self, connection, plan_uid, destination_guid):
        super(SecurityArchiveTmpAuth, self).__init__()
        self._connection = connection
        self._plan_uid = plan_uid
        self._destination_guid = destination_guid

    def get_tmp_auth_token(self):
        uri = u"/api/StorageAuthToken"
        data = {u"planUid": self._plan_uid, u"destinationGuid": self._destination_guid}
        response = self._connection.post(uri, data=json.dumps(data))
        return response


class StorageTokenProviderFactory(object):
    def __init__(self, connection, device_client):
        self._connection = connection
        self._device_client = device_client

    def create_security_archive_locator(self, plan_uid, destination_guid):
        return SecurityArchiveTmpAuth(self._connection, plan_uid, destination_guid)

    def create_backup_archive_locator(self, device_guid, destination_guid=None):
        if destination_guid is None:
            response = self._device_client.get_by_guid(
                device_guid, include_backup_usage=True
            )
            if destination_guid is None:
                # take the first destination guid we find
                destination_list = response["backupUsage"]
                if not destination_list:
                    raise Exception(
                        u"No destinations found for device guid: {}".format(device_guid)
                    )
                destination_guid = destination_list[0][u"targetComputerGuid"]

        return FileArchiveTmpAuth(
            self._connection, u"my", device_guid, destination_guid
        )
