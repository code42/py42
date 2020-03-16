class ArchiveModule(object):
    def __init__(self, archive_accessor_manager, archive_client):
        self._archive_accessor_manager = archive_accessor_manager
        self._archive_client = archive_client

    def stream_from_backup(self, file_path, device_guid, destination_guid=None):
        archive_accessor = self._archive_accessor_manager.get_archive_accessor(
            device_guid, destination_guid=destination_guid
        )

        return archive_accessor.stream_from_backup(file_path)

    def get_backup_sets(self, device_guid, destination_guid):
        return self._archive_client.get_backup_sets(device_guid, destination_guid)

    def get_data_key_token(self, device_guid):
        return self._archive_client.get_data_key_token(device_guid)

    def get_restore_history_by_org_id(self, days, org_id, page_num=None, page_size=None):
        return self._archive_client.get_restore_history(days, u"orgId", org_id, page_num, page_size)

    def get_restore_history_by_user_id(self, days, user_id, page_num=None, page_size=None):
        return self._archive_client.get_restore_history(
            days, u"userId", user_id, page_num, page_size
        )

    def get_restore_history_by_device_id(self, days, device_id, page_num=None, page_size=None):
        return self._archive_client.get_restore_history(
            days, u"computerId", device_id, page_num, page_size
        )

    def get_web_restore_info(self, src_guid, dest_guid):
        return self._archive_client.get_web_restore_info(src_guid, dest_guid)
