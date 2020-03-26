from py42.clients import BaseClient
from py42.clients.storage.archive import StorageArchiveClient
from py42.clients.storage.securitydata import StorageSecurityClient


class StorageClient(BaseClient):
    def __init__(self, session):
        super(StorageClient, self).__init__(session)
        self._archive_client = StorageArchiveClient(session)
        self._security_client = StorageSecurityClient(session)

    @property
    def archive(self):
        """A collection of methods related to storage archives."""
        return self._archive_client

    @property
    def securitydata(self):
        """A collection of methods related to security data found on storage nodes."""
        return self._security_client


class StorageClientFactory(object):
    def __init__(self, storage_session_manager, token_provider_factory):
        self._storage_session_manager = storage_session_manager
        self._token_provider_factory = token_provider_factory

    def from_device_guid(self, device_guid, destination_guid=None):
        """Creates a factory that produces
            :class:`py42.clients.storage.securitydata.StorageSecurityClient` objects for the
            device with the given GUID.

        Args:
            device_guid (str): The GUID for the device to create a storage client for.
            destination_guid (str, optional): The GUID for the destination containing the storage
                node that the device stores its archives on. If None, it will use the first one
                found. Defaults to None.

        Returns:
            :class:`py42.clients.storage.securitydata.StorageSecurityClient`
        """
        token_provider = self._token_provider_factory.create_backup_archive_locator(
            device_guid, destination_guid
        )
        session = self._storage_session_manager.get_storage_session(token_provider)
        return StorageClient(session)

    def from_plan_info(self, plan_uid, destination_guid):
        """Creates a factory that produces
            :class:`py42.clients.storage.securitydata.StorageSecurityClient` objects for the
            plan with the given UID.

        Args:
            plan_uid (str): The UID for the plan to create a
                :class:`py42.clients.storage.securitydata.StorageSecurityClient` factory for.
            destination_guid (str): The GUID for the destination containing the storage
                node that the device stores its archives on.

        Returns:
            :class:`py42.clients.storage.securitydata.StorageSecurityClient`
        """
        token_provider = self._token_provider_factory.create_security_archive_locator(
            plan_uid, destination_guid
        )
        session = self._storage_session_manager.get_storage_session(token_provider)
        return StorageClient(session)
