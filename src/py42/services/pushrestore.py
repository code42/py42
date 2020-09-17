from py42.services import BaseService


class PushRestoreService(BaseService):
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
        file_location=None,
        permit_restore_to_different_os_version=None,
        file_permissions=None,
        restore_full_path=None,
    ):
        """Submits a web restore job."""
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
            u"fileLocation": file_location,
            u"showDeleted": show_deleted,
            u"permitRestoreToDifferentOsVersion": permit_restore_to_different_os_version,
            u"filePermissions": file_permissions,
            u"restoreFullPath": restore_full_path,
        }
        return self._connection.post(uri, json=json_dict)
