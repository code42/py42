import json

from py42 import settings
from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class ArchiveClient(BaseClient):
    """A client for interacting with Code42 archive APIs."""

    def get_by_archive_guid(self, archive_guid):
        """Gets single archive information by GUID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            archive_guid (int): The GUID for the archive.

        Returns:
            :class:`py42.response.Py42Response`: A response containing archive information.
        """
        uri = u"/api/Archive/{}".format(archive_guid)
        return self._session.get(uri)

    def get_by_device_guid(self, device_guid):
        """Gets archive information for a device.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            device_guid (int): The GUID for the device.

        Returns:
            :class:`py42.response.Py42Response`: A response containing archive information.
        """
        uri = u"/api/Archive"
        params = dict(backupSourceGuid=device_guid)
        return self._session.get(uri, params=params)

    def get_by_user_uid(self, user_uid):
        """Gets archive information for a user.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            user_uid (int): The userUid for a user.

        Returns:
            :class:`py42.response.Py42Response`: A response containing archive information.
        """
        uri = u"/api/Archive"
        params = dict(userUid=user_uid)
        return self._session.get(uri, params=params)

    def get_page(self, page_num, page_size=None, **kwargs):
        """Gets an individual page of archives.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
            page_num (int): The page number to request.
            page_size (int, optional): The number of archives to return per page.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = u"/api/Archive"
        page_size = page_size or settings.items_per_page
        params = dict(
            pgNum=page_num,
            pgSize=page_size,
            **kwargs
        )
        return self._session.get(uri, params=params)

    def get_by_user_uid_list(self, user_uid_list):
        """Gets archive information for a list of userUids.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Archive-get>`__

        Args:
             user_uid_list (list): A list of userUids.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of archives.
        """
        return get_all_pages(
            self.get_page,
            u"archives",
            userUid=','.join(map(str, user_uid_list)),
        )





