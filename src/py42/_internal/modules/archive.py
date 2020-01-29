from py42._internal.archive_access import ArchiveAccessorManager
from py42._internal.clients.archive import ArchiveClient


class ArchiveModule(object):
    def __init__(self, archive_accessor_manager, archive_client):
        # type: (ArchiveAccessorManager, ArchiveClient) -> None
        self._archive_accessor_manager = archive_accessor_manager
        self._archive_client = archive_client

    def download_from_backup(
        self, file_path, device_guid, destination_guid=None, save_as_dir=None, save_as_filename=None
    ):
        archive_accessor = self._archive_accessor_manager.get_archive_accessor(
            device_guid, destination_guid=destination_guid
        )

        return archive_accessor.download_from_backup(file_path, save_as_dir, save_as_filename)

    def get_backup_sets(self, device_guid, destination_guid):
        return self._archive_client.get_backup_sets(device_guid, destination_guid)

    def get_data_key_token(self, computer_guid):
        return self._archive_client.get_data_key_token(computer_guid)

    def get_restore_history(self, days, org_id=None, page_num=None, page_size=None):
        return self._archive_client.get_restore_history(days, org_id, page_num, page_size)

    def get_web_restore_info(self, src_guid, dest_guid):
        return self._archive_client.get_web_restore_info(src_guid, dest_guid)
