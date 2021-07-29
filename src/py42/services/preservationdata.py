from urllib.parse import quote

from py42.services import BaseService


class PreservationDataService(BaseService):
    def find_file_version(self, file_md5, file_sha256, paths):
        """Fetch file version details.

        Args:
            file_md5 (str): MD5 encoded hash of the file.
            file_sha256 (str): SHA256 encoded hash of the file.
            paths (str): File path with filename to fetch.

        Returns:
            :class:`py42.response.Py42Response`
        """

        data = {"fileSHA256": file_sha256, "fileMD5": file_md5, "devicePaths": paths}
        uri = "/api/v1/FindAvailableVersion"
        return self._connection.post(uri, json=data)

    def get_file_version_list(self, deviceGuid, file_md5, file_sha256, path):
        params = "fileSHA256={}&fileMD5={}&deviceGuid={}&path={}"
        params = params.format(file_sha256, file_md5, deviceGuid, quote(path))
        uri = f"/api/v1/FileVersionListing?{params}"
        return self._connection.get(uri)
