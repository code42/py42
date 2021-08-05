from py42._compat import quote
from py42.services import BaseService


class ExfiltratedDataService(BaseService):

    _base_uri = u"api/v1/"

    def __init__(self, main_session, streaming_session):
        super(ExfiltratedDataService, self).__init__(main_session)
        self._streaming_session = streaming_session

    def get_download_token(self, event_id, device_id, file_path, timestamp):
        """Get EDS download token for a file.

        Args:
            event_id (str): Id of the file event that references the file desired for download.
            device_id (str): Id of the device on which the file desired for download is stored.
            file_path (str): Path where the file desired for download resides on the device.
            timestamp (int): Last updated timestamp of the file in milliseconds.

        Returns:
            :class:`py42.response.Py42Response`: A response containing download token for the file.
        """
        params = u"deviceUid={}&eventId={}&filePath={}&versionTimestamp={}"
        params = params.format(device_id, event_id, quote(file_path), timestamp)
        resource = u"file-download-token"
        uri = u"{}{}?{}".format(self._base_uri, resource, params)
        return self._connection.get(uri)

    def get_file(self, token):
        """Streams a file.

        Args:
            token (str):EDS Download token.

        Returns:
            Returns a stream of the file indicated by the input token.
        """
        resource = u"get-file"
        uri = u"{}/{}{}".format(self._connection.host_address, self._base_uri, resource)
        params = {u"token": token}
        headers = {u"Accept": u"*/*"}
        return self._streaming_session.get(
            uri, params=params, headers=headers, stream=True
        )
