from py42.clients import BaseClient
import requests


class StorageNodeClient(BaseClient):

    _base_uri = u"c42api/v3/"

    def __init__(self, session, archive_guid, file_id, timestamp):
        super(StorageNodeClient, self).__init__(session)
        self._archive_guid = archive_guid
        self._file_id = file_id
        self._timestamp = timestamp

    def get_download_token(self):

        params = "archiveGuid={0}&fileId={1}&versionTimestamp={2}".format(
            self._archive_guid, self._file_id, self._timestamp
        )
        resource = u"FileDownloadToken"
        uri = "{0}{1}?{2}".format(self._base_uri, resource, params)
        return self._session.get(uri)

    def get_file(self, host_address, token, file):
        resource = u"GetFile"
        uri = "{0}/{1}{2}?{3}".format(host_address, self._base_uri, resource, token)
        with requests.get(uri, stream=True) as reader:
            with open(file, "wb") as local_file:
                local_file.write(reader.content)
