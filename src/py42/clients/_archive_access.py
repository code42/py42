import posixpath
from collections import namedtuple

from py42.exceptions import Py42ArchiveFileNotFoundError
from py42.clients._archiveaccess.polling import create_file_size_poller
from py42.clients._archiveaccess.polling import create_restore_job_manager


FileSelection = namedtuple(
    u"FileSelection", u"file, num_files, num_dirs, num_bytes"
)


class FileType(object):
    DIRECTORY = u"DIRECTORY"
    FILE = u"FILE"


class ArchiveAccessorManager(object):
    def __init__(self, archive_service, storage_service_factory, devices_service):
        self._archive_service = archive_service
        self._storage_service_factory = storage_service_factory
        self._devices_service = devices_service

    def get_archive_accessor(
        self,
        device_guid,
        destination_guid=None,
        private_password=None,
        encryption_key=None,
        use_push=False,
    ):
        decryption_keys = self._get_decryption_keys(
            device_guid=device_guid,
            private_password=private_password,
            encryption_key=encryption_key,
        )

        if use_push:
            storage_archive_service = self._storage_service_factory.create_push_restore_service(device_guid)
        else:
            storage_archive_service = self._storage_service_factory.create_archive_service(
                device_guid, destination_guid=destination_guid
            )

        session_id = self._create_restore_session(
            storage_archive_service, device_guid, **decryption_keys
        )
        restore_job_manager = create_restore_job_manager(
            archive_service=self._archive_service,
            storage_archive_service=storage_archive_service,
            device_guid=device_guid,
            archive_session_id=session_id,
        )
        file_size_poller = create_file_size_poller(storage_archive_service, device_guid)
        node_guid = self._get_first_node_guid(device_guid)
        return ArchiveAccessor(
            device_guid=device_guid,
            node_guid=node_guid,
            archive_session_id=session_id,
            storage_archive_service=storage_archive_service,
            restore_job_manager=restore_job_manager,
            file_size_poller=file_size_poller,
        )

    def _get_decryption_keys(self, device_guid, private_password, encryption_key):
        decryption_keys = {}
        if encryption_key:
            decryption_keys[u"encryption_key"] = encryption_key
        else:
            data_key_token = (
                self._get_data_key_token(device_guid) if not encryption_key else None
            )
            if data_key_token:
                decryption_keys[u"data_key_token"] = data_key_token

            if private_password:
                decryption_keys[u"private_password"] = private_password
        return decryption_keys

    def _get_data_key_token(self, device_guid):
        return self._archive_service.get_data_key_token(device_guid)[u"dataKeyToken"]

    def _get_first_node_guid(self, device_guid):
        response = self._devices_service.get_by_guid(device_guid, include_backup_usage=True)
        return response[u"backupUsage"][0][u"serverGuid"]

    @staticmethod
    def _create_restore_session(session_creator, device_guid, **kwargs):
        response = session_creator.create_restore_session(device_guid, **kwargs)
        return response[u"webRestoreSessionId"]


def _create_file_selections(file_paths, metadata_list, file_sizes=None):
    file_selections = []
    for i in range(0, len(file_paths)):
        metadata = metadata_list[i]
        size_info = file_sizes[i] if file_sizes else _get_default_file_size()
        file = {
            u"fileType": metadata[u"type"].upper(),
            u"path": metadata[u"path"],
            u"selected": True,
        }
        selection = FileSelection(
            file=file,
            num_files=size_info[u"numFiles"],
            num_dirs=size_info[u"numDirs"],
            num_bytes=size_info[u"size"],
        )
        file_selections.append(selection)
    return file_selections


class ArchiveAccessor(object):
    DEFAULT_DIRECTORY_DOWNLOAD_NAME = u"download"
    JOB_POLLING_INTERVAL = 1

    def __init__(
        self,
        device_guid,
        node_guid,
        archive_session_id,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        self._device_guid = device_guid
        self._node_guid = node_guid
        self._archive_session_id = archive_session_id
        self._storage_archive_service = storage_archive_service
        self._restore_job_manager = restore_job_manager
        self._file_size_poller = file_size_poller

    def stream_from_backup(self, file_paths, file_size_calc_timeout=None):
        file_selections = self._create_file_selections(
            file_paths, file_size_calc_timeout
        )
        return self._restore_job_manager.get_stream(file_selections)

    def stream_to_destination(
        self, restore_path, accepting_guid, file_paths, file_size_calc_timeout=None,
    ):
        file_selections = self._create_file_selections(
            file_paths, file_size_calc_timeout
        )
        return self._restore_job_manager.send_stream(
            restore_path=restore_path,
            node_guid=self._node_guid,
            accepting_guid=accepting_guid,
            file_selections=file_selections,
        )

    def _create_file_selections(self, file_paths, file_size_calc_timeout):
        if not isinstance(file_paths, (list, tuple)):
            file_paths = [file_paths]
        file_paths = [fp.replace(u"\\", u"/") for fp in file_paths]
        #metadata_list = self._get_restore_metadata(file_paths)
        #file_ids = [md[u"id"] for md in metadata_list]
        # file_sizes = self._file_size_poller.get_file_sizes(
        #     file_ids, timeout=file_size_calc_timeout
        # )
        #return _create_file_selections(file_paths, metadata_list, file_sizes)
        return [FileSelection({"fileType": "FILE", "path": p, "selected": True}, 1, 1, 1) for p in file_paths]

    def _get_restore_metadata(self, file_paths):
        metadata_list = []
        for path in file_paths:
            metadata = self._get_file_via_walking_tree(path)
            metadata_list_entry = {
                u"id": metadata[u"id"],
                u"path": metadata[u"path"],
                u"type": metadata[u"type"],
            }
            metadata_list.append(metadata_list_entry)
        return metadata_list

    def _get_file_via_walking_tree(self, file_path):
        path_parts = file_path.split(u"/")
        path_root = path_parts[0] + u"/"

        response = self._get_children(file_id=None)
        for root in response:
            if root[u"path"].lower() == path_root.lower():
                return self._walk_tree(response, root, path_parts[1:])

        raise Py42ArchiveFileNotFoundError(response, self._device_guid, file_path)

    def _walk_tree(self, response, current_file, remaining_path_components):
        if not remaining_path_components or not remaining_path_components[0]:
            return current_file

        children = self._get_children(file_id=current_file[u"id"])
        current_path = current_file[u"path"]
        target_child_path = posixpath.join(current_path, remaining_path_components[0])

        for child in children:
            if child[u"path"].lower() == target_child_path.lower():
                return self._walk_tree(response, child, remaining_path_components[1:])

        raise Py42ArchiveFileNotFoundError(
            response, self._device_guid, target_child_path
        )

    def _get_children(self, file_id=None):
        return self._storage_archive_service.get_file_path_metadata(
            self._archive_session_id,
            self._device_guid,
            file_id=file_id,
            show_deleted=True,
        )


def _get_default_file_size():
    return {u"numFiles": 1, u"numDirs": 1, u"size": 1}
