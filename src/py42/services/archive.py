from py42 import settings
from py42.services import BaseService
from py42.services.util import get_all_pages


class ArchiveService(BaseService):
    def get_data_key_token(self, device_guid):
        uri = u"/api/DataKeyToken"
        data = {u"computerGuid": device_guid}
        return self._connection.post(uri, json=data)

    def get_single_archive(self, archive_guid):
        """Gets single archive information by GUID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            archive_guid (str): The GUID for the archive.

        Returns:
            :class:`py42.response.Py42Response`: A response containing archive information.
        """
        uri = u"/api/Archive/{}".format(archive_guid)
        return self._connection.get(uri)

    def get_page(self, page_num, page_size=None, **kwargs):
        """Gets an individual page of archives.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            page_num (int): The page number to request.
            page_size (int, optional): The number of archives to return per page. Defaults to `py42.settings.items_per_page`.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/Archive"
        page_size = page_size or settings.items_per_page
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._connection.get(uri, params=params)

    def get_all_archives_from_value(self, id_value, id_type):
        """Gets archive information from an ID, such as a User UID, Device GUID, or Destination GUID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            id_value (str): Query value for archive.
            id_type (str): API query value description (e.g backupSourceGuid,
                userUid, destinationGuid)

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of archives.
        """
        params = {u"{}".format(id_type): u"{}".format(id_value)}
        return get_all_pages(self.get_page, u"archives", **params)

    def get_backup_sets(self, device_guid, destination_guid):
        uri = u"/c42api/v3/BackupSets/{}/{}".format(device_guid, destination_guid)
        return self._connection.get(uri)

    def get_all_restore_history(self, days, id_type, id_value, **kwargs):
        return get_all_pages(
            self._get_restore_history_page,
            u"restoreEvents",
            days=days,
            id_type=id_type,
            id_value=id_value,
            **kwargs
        )

    def _get_restore_history_page(
        self, days, id_type, id_value, page_num, page_size, **kwargs
    ):
        uri = u"/api/RestoreHistory"
        params = dict(days=days, pgNum=page_num, pgSize=page_size, **kwargs)
        params[id_type] = id_value
        return self._connection.get(uri, params=params)

    def get_web_restore_info(self, src_guid, dest_guid):
        uri = u"/api/WebRestoreInfo"
        params = {u"srcGuid": src_guid, u"destGuid": dest_guid}
        return self._connection.get(uri, params=params)

    def _get_cold_storage_archives_page(
        self,
        org_id=None,
        include_child_orgs=None,
        sort_key=u"archiveHoldExpireDate",
        sort_dir=u"asc",
        page_size=None,
        page_num=None,
    ):
        uri = u"/api/ColdStorage"
        params = {
            u"orgId": org_id,
            u"incChildOrgs": include_child_orgs,
            u"srtKey": sort_key,
            u"srtDir": sort_dir,
            u"pgSize": page_size,
            u"pgNum": page_num,
        }

        return self._connection.get(uri, params=params)

    def get_all_org_cold_storage_archives(
        self,
        org_id,
        include_child_orgs=True,
        sort_key=u"archiveHoldExpireDate",
        sort_dir=u"asc",
    ):
        return get_all_pages(
            self._get_cold_storage_archives_page,
            u"coldStorageRows",
            org_id=org_id,
            include_child_orgs=include_child_orgs,
            sort_key=sort_key,
            sort_dir=sort_dir,
        )

    def update_cold_storage_purge_date(self, archive_guid, purge_date):
        uri = u"/api/coldStorage/{}".format(archive_guid)
        params = {u"idType": u"guid"}
        data = {u"archiveHoldExpireDate": purge_date}
        return self._connection.put(uri, params=params, json=data)
