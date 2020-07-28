from py42.clients import BaseClient


class PreservationDataServiceClient(BaseClient):
    def find_file_versions(self, file_md5, file_sha256, device_id, paths):
        """Fetch file version details.

        Args:
            file_md5 (str): MD5 encoded hash of the file.
            file_sha256 (str): SHA256 encoded hash of the file.
            device_id (str): Id of the device where the files are from.
            paths (str): File path with filename to fetch.

        Returns:
            :class:`py42.response.Py42Response`
        """

        data = {
            u"fileSHA256": file_sha256,
            u"fileMD5": file_md5,
            u"devicePaths": [{u"deviceGuid": device_id, u"paths": paths}],
        }
        uri = u"/api/v1/FindAvailableVersion"
        return self._session.post(uri, json=data)
