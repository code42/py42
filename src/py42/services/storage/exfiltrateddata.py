from urllib.parse import quote

from py42.services import BaseService


class ExfiltratedDataService(BaseService):

    _base_uri = "api/v1/"

    def __init__(self, main_session, streaming_session):
        super().__init__(main_session)
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
        params = "deviceUid={}&eventId={}&filePath={}&versionTimestamp={}"
        params = params.format(device_id, event_id, quote(file_path), timestamp)
        resource = "file-download-token"
        headers = {"Accept": "*/*"}
        uri = f"{self._base_uri}{resource}?{params}"
        return self._connection.get(uri, headers=headers)

    def get_file(self, token):
        """Streams a file.

        Args:
            token (str):EDS Download token.

        Returns:
            Returns a stream of the file indicated by the input token.
        """
        resource = "get-file"
        uri = f"{self._connection.host_address}/{self._base_uri}{resource}"
        params = {"token": token}
        headers = {"Accept": "*/*"}
        return self._streaming_session.get(
            uri, params=params, headers=headers, stream=True
        )
