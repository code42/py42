from py42.services import BaseService


class ExfiltratedDataService(BaseService):

    _base_uri = "api/v1/"

    def __init__(self, main_connection, streaming_session):
        super().__init__(main_connection)
        self._streaming_session = streaming_session

    def get_download_token(self, downloadRequestUrl):
        """Get EDS download token for a file.

        Args:
            downloadRequestUrl (str): The download request url to get the token

        Returns:
            :class:`py42.response.Py42Response`: A response containing download token for the file.
        """
        headers = {"Accept": "*/*"}
        uri = f"{downloadRequestUrl}"
        return self._connection.get(uri, headers=headers)

    def get_file(self, token):
        """Streams a file.

        Args:
            token (str):EDS Download token.

        Returns:
            Returns a stream of the file indicated by the input token.
        """
        uri = f"{token}"
        headers = {"Accept": "*/*"}
        return self._streaming_session.get(uri, headers=headers, stream=True)
