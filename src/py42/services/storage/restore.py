from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42BadRestoreRequestError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42InvalidArchiveEncryptionKey
from py42.exceptions import Py42InvalidArchivePassword
from py42.services import BaseService


class PushRestoreLocation:
    ORIGINAL_LOCATION = "ORIGINAL_LOCATION"
    TARGET_DIRECTORY = "TARGET_DIRECTORY"


class PushRestoreExistingFiles:
    OVERWRITE_ORIGINAL = "OVERWRITE_ORIGINAL"
    RENAME_ORIGINAL = "RENAME_ORIGINAL"


class RestoreService(BaseService):
    def create_restore_session(
        self,
        device_guid,
        data_key_token=None,
        private_password=None,
        encryption_key=None,
    ):
        """Creates a web restore connection."""
        uri = "/api/v1/WebRestoreSession"
        json_dict = {
            "computerGuid": device_guid,
            "dataKeyToken": data_key_token,
            "privatePassword": private_password,
            "encryptionKey": encryption_key,
        }
        try:
            return self._connection.post(uri, json=json_dict)
        except Py42InternalServerError as err:
            if "PRIVATE_PASSWORD_INVALID" in err.response.text:
                raise Py42InvalidArchivePassword(err)
            elif "CUSTOM_KEY_INVALID" in err.response.text:
                raise Py42InvalidArchiveEncryptionKey(err)
            raise

    def get_restore_status(self, job_id):
        uri = f"/api/v1/WebRestoreJob/{job_id}"
        return self._connection.get(uri)


class PushRestoreService(RestoreService):
    """A service for creating Push Restores."""

    def start_push_restore(
        self,
        device_guid,
        accepting_device_guid,
        web_restore_session_id,
        node_guid,
        restore_path,
        restore_groups,
        num_files,
        num_bytes,
        show_deleted=None,
        permit_restore_to_different_os_version=None,
        file_permissions=None,
        restore_full_path=None,
        file_location=None,
        existing_files=None,
    ):
        """Submits a push restore job."""
        uri = "/api/v9/restore/push"
        json_dict = {
            "sourceComputerGuid": device_guid,
            "acceptingComputerGuid": accepting_device_guid,
            "webRestoreSessionId": web_restore_session_id,
            "targetNodeGuid": node_guid,
            "restorePath": restore_path,
            "restoreGroups": restore_groups,
            "numFiles": num_files,
            "numBytes": num_bytes,
            "showDeleted": show_deleted,
            "permitRestoreToDifferentOsVersion": permit_restore_to_different_os_version,
            "filePermissions": file_permissions,
            "restoreFullPath": restore_full_path,
            "fileLocation": file_location,
            "existingFiles": existing_files,
        }
        try:
            return self._connection.post(uri, json=json_dict)
        except Py42BadRequestError as err:
            if "CREATE_FAILED" in err.response.text:
                raise Py42BadRestoreRequestError(err)
            raise
