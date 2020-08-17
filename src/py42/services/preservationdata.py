from py42._compat import quote, urlencode
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

        data = {
            u"fileSHA256": file_sha256,
            u"fileMD5": file_md5,
            u"devicePaths": paths,
        }
        uri = u"/api/v1/FindAvailableVersion"
        return self._connection.post(uri, json=data)

    def get_file_version_list(self, deviceGuid, file_md5, file_sha256, path):
        params = {"fileSHA256": file_sha256, "fileMD5": file_md5, "deviceGuid": deviceGuid, "path": path}
        params = urlencode(params, quote_via=quote)
        uri = u"/api/v1/FileVersionListing?{}".format(params)
        print(uri)
        return self._connection.get(uri)
