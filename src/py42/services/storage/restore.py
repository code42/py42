from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42BadRestoreRequestError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42InvalidArchiveEncryptionKey
from py42.exceptions import Py42InvalidArchivePassword
from py42.services import BaseService


class PushRestoreLocation:
    ORIGINAL_LOCATION = u"ORIGINAL_LOCATION"
    TARGET_DIRECTORY = u"TARGET_DIRECTORY"


class PushRestoreExistingFiles:
    OVERWRITE_ORIGINAL = u"OVERWRITE_ORIGINAL"
    RENAME_ORIGINAL = u"RENAME_ORIGINAL"


class RestoreService(BaseService):
    def create_restore_session(
        self,
        device_guid,
        data_key_token=None,
        private_password=None,
        encryption_key=None,
    ):
        """Creates a web restore connection.
        See https://console.us.code42.com/apidocviewer/#WebRestoreSession
        """
        uri = u"/api/WebRestoreSession"
        json_dict = {
            u"computerGuid": device_guid,
            u"dataKeyToken": data_key_token,
            u"privatePassword": private_password,
            u"encryptionKey": encryption_key,
        }
        try:
            return self._connection.post(uri, json=json_dict)
        except Py42InternalServerError as err:
            if u"PRIVATE_PASSWORD_INVALID" in err.response.text:
                raise Py42InvalidArchivePassword(err)
            elif u"CUSTOM_KEY_INVALID" in err.response.text:
                raise Py42InvalidArchiveEncryptionKey(err)
            raise

    def get_restore_status(self, job_id):
        uri = u"/api/WebRestoreJob/{}".format(job_id)
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
        uri = u"/api/v9/restore/push"
        json_dict = {
            u"sourceComputerGuid": device_guid,
            u"acceptingComputerGuid": accepting_device_guid,
            u"webRestoreSessionId": web_restore_session_id,
            u"targetNodeGuid": node_guid,
            u"restorePath": restore_path,
            u"restoreGroups": restore_groups,
            u"numFiles": num_files,
            u"numBytes": num_bytes,
            u"showDeleted": show_deleted,
            u"permitRestoreToDifferentOsVersion": permit_restore_to_different_os_version,
            u"filePermissions": file_permissions,
            u"restoreFullPath": restore_full_path,
            u"fileLocation": file_location,
            u"existingFiles": existing_files,
        }
        try:
            return self._connection.post(uri, json=json_dict)
        except Py42BadRequestError as err:
            if u"CREATE_FAILED" in err.response.text:
                raise Py42BadRestoreRequestError(err)
            raise
