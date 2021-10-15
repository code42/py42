from py42 import settings
from py42.services import BaseService
from py42.services.util import get_all_pages


class ArchiveService(BaseService):
    def get_data_key_token(self, device_guid):
        uri = "/api/v1/DataKeyToken"
        data = {"computerGuid": device_guid}
        return self._connection.post(uri, json=data)

    def get_single_archive(self, archive_guid):
        """Gets single archive information by GUID.

        Args:
            archive_guid (str): The GUID for the archive.

        Returns:
            :class:`py42.response.Py42Response`: A response containing archive information.
        """
        uri = f"/api/v1/Archive/{archive_guid}"
        return self._connection.get(uri)

    def get_page(self, page_num, page_size=None, **kwargs):
        """Gets an individual page of archives.

        Args:
            page_num (int): The page number to request.
            page_size (int, optional): The number of archives to return per page. Defaults to `py42.settings.items_per_page`.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v1/Archive"
        page_size = page_size or settings.items_per_page
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._connection.get(uri, params=params)

    def get_all_archives_from_value(self, id_value, id_type):
        """Gets archive information from an ID, such as a User UID, Device GUID, or Destination GUID.

        Args:
            id_value (str): Query value for archive.
            id_type (str): API query value description (e.g backupSourceGuid,
                userUid, destinationGuid)

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of archives.
        """
        params = {id_type: id_value}
        return get_all_pages(self.get_page, "archives", **params)

    def get_backup_sets(self, device_guid, destination_guid):
        uri = f"/api/v3/BackupSets/{device_guid}/{destination_guid}"
        return self._connection.get(uri)

    def get_all_restore_history(self, days, id_type, id_value, **kwargs):
        return get_all_pages(
            self._get_restore_history_page,
            "restoreEvents",
            days=days,
            id_type=id_type,
            id_value=id_value,
            **kwargs,
        )

    def _get_restore_history_page(
        self, days, id_type, id_value, page_num, page_size, **kwargs
    ):
        uri = "/api/v1/RestoreHistory"
        params = dict(days=days, pgNum=page_num, pgSize=page_size, **kwargs)
        params[id_type] = id_value
        return self._connection.get(uri, params=params)

    def get_web_restore_info(self, src_guid, dest_guid):
        uri = "/api/v1/WebRestoreInfo"
        params = {"srcGuid": src_guid, "destGuid": dest_guid}
        return self._connection.get(uri, params=params)

    def _get_cold_storage_archives_page(
        self,
        org_id=None,
        include_child_orgs=None,
        sort_key="archiveHoldExpireDate",
        sort_dir="asc",
        page_size=None,
        page_num=None,
    ):
        uri = "/api/v1/ColdStorage"
        params = {
            "orgId": org_id,
            "incChildOrgs": include_child_orgs,
            "srtKey": sort_key,
            "srtDir": sort_dir,
            "pgSize": page_size,
            "pgNum": page_num,
        }

        return self._connection.get(uri, params=params)

    def get_all_org_cold_storage_archives(
        self,
        org_id,
        include_child_orgs=True,
        sort_key="archiveHoldExpireDate",
        sort_dir="asc",
    ):
        return get_all_pages(
            self._get_cold_storage_archives_page,
            "coldStorageRows",
            org_id=org_id,
            include_child_orgs=include_child_orgs,
            sort_key=sort_key,
            sort_dir=sort_dir,
        )

    def update_cold_storage_purge_date(self, archive_guid, purge_date):
        uri = f"/api/v1/coldStorage/{archive_guid}"
        params = {"idType": "guid"}
        data = {"archiveHoldExpireDate": purge_date}
        return self._connection.put(uri, params=params, json=data)
