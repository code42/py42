from urllib.parse import quote

from py42.services import BaseService


class PreservationDataService(BaseService):
    def get_file_version_list(self, device_id, file_md5, file_sha256, path):
        params = "fileSHA256={}&fileMD5={}&deviceUid={}&filePath={}"
        params = params.format(file_sha256, file_md5, device_id, quote(path))
        uri = f"/api/v3/search-file?{params}"
        return self._connection.get(uri)
