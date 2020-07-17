from py42.clients import BaseClient


class StoragePreservationDataClient(BaseClient):

    _base_uri = u"c42api/v3/"

    def __init__(self, main_session, streaming_session):
        super(StoragePreservationDataClient, self).__init__(main_session)
        self._streaming_session = streaming_session

    def get_download_token(self, archive_guid, file_id, timestamp):
        """Get PDS download token for a file.

        Args:
            archive_guid (str): Archive guid of the file
            file_id (str): Id of the file.
            timestamp (int): Last updated timestamp of the file in milliseconds.

        Returns:
            :class:`py42.response.Py42Response`: A response containing download token for the file.
        """
        params = {
            u"archiveGuid": archive_guid,
            u"fileId": file_id,
            u"versionTimestamp": timestamp,
        }
        resource = u"FileDownloadToken"
        uri = "{}{}".format(self._base_uri, resource)
        return self._session.get(uri, params=params)

    def get_file(self, token):
        """Streams a file.

        Args:
            token (str): PDS Download token.

        Returns:
            Returns a stream of the requested token.
        """
        resource = u"GetFile"
        uri = u"{}/{}{}".format(self._session.host_address, self._base_uri, resource)
        if u"PDSDownloadToken=" in token:
            replaced_token = token.replace(u"PDSDownloadToken=", "")
        else:
            replaced_token = token
        params = {u"PDSDownloadToken": replaced_token}
        headers = {u"Accept": "*/*"}
        return self._streaming_session.get(
            uri, params=params, headers=headers, stream=True
        )
