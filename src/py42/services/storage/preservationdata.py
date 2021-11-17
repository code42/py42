from py42.services import BaseService


class StoragePreservationDataService(BaseService):

    _base_uri = "api/v3/"

    def __init__(self, main_session, streaming_session):
        super().__init__(main_session)
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
            "archiveGuid": archive_guid,
            "fileId": file_id,
            "versionTimestamp": timestamp,
        }
        resource = "FileDownloadToken"
        uri = f"{self._base_uri}{resource}"
        return self._connection.get(uri, params=params)

    def get_file(self, token):
        """Streams a file.

        Args:
            token (str): PDS Download token.

        Returns:
            Returns a stream of the requested token.
        """
        resource = "GetFile"
        uri = f"{self._connection.host_address}/{self._base_uri}{resource}"
        if "PDSDownloadToken=" in token:
            replaced_token = token.replace("PDSDownloadToken=", "")
        else:
            replaced_token = token
        params = {"PDSDownloadToken": replaced_token}
        headers = {"Accept": "*/*"}
        return self._streaming_session.get(
            uri, params=params, headers=headers, stream=True
        )
