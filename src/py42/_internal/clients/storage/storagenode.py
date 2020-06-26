from py42.clients import BaseClient
import requests


class StoragePreservationDataClient(BaseClient):

    _base_uri = u"c42api/v3/"

    def __init__(self, session):
        super(StoragePreservationDataClient, self).__init__(session)

    def get_download_token(self, archive_guid, file_id, timestamp):
        """Get PDS download token of a file.

        Args:
            archive_guid (str): Archive guid of the file
            file_id (str): Id of the file.
            timestamp (int): Last updated timestamp of the file.

        Returns:
            :class:`py42.response.Py42Response`: A response containing download token of the file.
        """
        params = {
            u"archiveGuid": archive_guid,
            u"fileId": file_id,
            u"versionTimestamp": timestamp,
        }
        resource = u"FileDownloadToken"
        uri = "{0}{1}".format(self._base_uri, resource)
        return self._session.get(uri, params=params)

    def get_file(self, token):
        """Streams a file.

        Args:
            token (str): PDS Download token.

        Returns:
            Returns a stream of the requested token.
        """
        resource = u"GetFile"
        uri = "{0}/{1}{2}".format(self._session.host_address, self._base_uri, resource)
        if u"PDSDownloadToken=" in token:
            token = token.replace(u"PDSDownloadToken= ", "")
        params = {u"PDSDownloadToken": token}
        return requests.get(uri, params=params, stream=True)
