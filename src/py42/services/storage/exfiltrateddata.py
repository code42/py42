from py42.services import BaseService


class ExfiltratedDataService(BaseService):

    _base_uri = "api/v1/"

    def __init__(self, main_connection, streaming_session):
        super().__init__(main_connection)
        self._streaming_session = streaming_session

    def get_file(self, downloadUrl):
        """Streams a file.

        Args:
            token (str):EDS Download token.

        Returns:
            Returns a stream of the file indicated by the input token.
        """
        uri = f"{downloadUrl}"
        headers = {"Accept": "*/*"}
        return self._streaming_session.get(uri, headers=headers, stream=True)
