import posixpath
from collections import namedtuple

from py42.exceptions import Py42ArchiveFileNotFoundError

# Data for initiating a web or push restore.
FileSelection = namedtuple("FileSelection", "file, num_files, num_dirs, num_bytes")


class FileType:
    """The different file-types in an archive."""

    DIRECTORY = "DIRECTORY"
    FILE = "FILE"


class ArchiveAccessor:
    """Base class for certain archive operations, such file-exploring or restoring."""

    DEFAULT_DIRECTORY_DOWNLOAD_NAME = "download"
    JOB_POLLING_INTERVAL = 1

    def __init__(
        self,
        device_guid,
        archive_session_id,
        destination_guid,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        self._device_guid = device_guid
        self._archive_session_id = archive_session_id
        self.destination_guid = destination_guid
        self._storage_archive_service = storage_archive_service
        self._restore_job_manager = restore_job_manager
        self._file_size_poller = file_size_poller


class ArchiveExplorer(ArchiveAccessor):
    """Abstracts file exploring / tree-navigation in the context of a restore."""

    def create_file_selections(self, backup_set_id, file_paths, file_size_calc_timeout):
        if not isinstance(file_paths, (list, tuple)):
            file_paths = [file_paths]
        file_paths = [fp.replace("\\", "/") for fp in file_paths]
        metadata_list = self._get_restore_metadata(backup_set_id, file_paths)
        file_ids = [md["id"] for md in metadata_list]
        file_sizes = self._file_size_poller.get_file_sizes(
            file_ids, timeout=file_size_calc_timeout
        )
        return _create_file_selections(file_paths, metadata_list, file_sizes)

    def _get_restore_metadata(self, backup_set_id, file_paths):
        metadata_list = []
        for path in file_paths:
            metadata = self._get_file_via_walking_tree(backup_set_id, path)
            metadata_list_entry = {
                "id": metadata["id"],
                "path": metadata["path"],
                "type": metadata["type"],
            }
            metadata_list.append(metadata_list_entry)
        return metadata_list

    def _get_file_via_walking_tree(self, backup_set_id, file_path):
        path_parts = file_path.split("/")
        path_root = path_parts[0] + "/"

        response = self._get_children(backup_set_id, file_id=None)
        for root in response:
            if root["path"].lower() == path_root.lower():
                return self._walk_tree(backup_set_id, response, root, path_parts[1:])

        raise Py42ArchiveFileNotFoundError(response, self._device_guid, file_path)

    def _walk_tree(
        self, backup_set_id, response, current_file, remaining_path_components
    ):
        if not remaining_path_components or not remaining_path_components[0]:
            return current_file

        children = self._get_children(backup_set_id, file_id=current_file["id"])
        current_path = current_file["path"]
        target_child_path = posixpath.join(current_path, remaining_path_components[0])

        for child in children:
            if child["path"].lower() == target_child_path.lower():
                return self._walk_tree(
                    backup_set_id, response, child, remaining_path_components[1:]
                )

        raise Py42ArchiveFileNotFoundError(
            response, self._device_guid, target_child_path
        )

    def _get_children(self, backup_set_id, file_id=None):
        return self._storage_archive_service.get_file_path_metadata(
            self._archive_session_id,
            self._device_guid,
            backup_set_id,
            file_id=file_id,
            show_deleted=True,
        )


class ArchiveContentStreamer(ArchiveExplorer):
    """A class with methods for restoring files from backup."""

    def stream_from_backup(
        self,
        backup_set_id,
        file_paths,
        file_size_calc_timeout=None,
        show_deleted=None,
    ):
        file_selections = self.create_file_selections(
            backup_set_id, file_paths, file_size_calc_timeout
        )
        return self._restore_job_manager.get_stream(
            backup_set_id, file_selections, show_deleted=show_deleted
        )


class ArchiveContentPusher(ArchiveAccessor):
    """A class with methods for restoring files from backup and pushing them to a device
    (push restore)."""

    def __init__(
        self,
        device_guid,
        destination_guid,
        node_guid,
        archive_session_id,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        self._node_guid = node_guid
        super().__init__(
            device_guid,
            archive_session_id,
            destination_guid,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )

    def stream_to_device(
        self,
        restore_path,
        accepting_guid,
        file_selections,
        backup_set_id,
        show_deleted,
        overwrite_existing_files,
    ):
        return self._restore_job_manager.send_stream(
            restore_path,
            self._node_guid,
            accepting_guid,
            file_selections,
            backup_set_id,
            show_deleted,
            overwrite_existing_files,
        )


def _create_file_selections(file_paths, metadata_list, file_sizes=None):
    file_selections = []
    for i in range(0, len(file_paths)):
        metadata = metadata_list[i]
        size_info = file_sizes[i] if file_sizes else _get_default_file_size()
        file = {
            "fileType": metadata["type"].upper(),
            "path": metadata["path"],
            "selected": True,
        }
        selection = FileSelection(
            file,
            size_info["numFiles"],
            size_info["numDirs"],
            size_info["size"],
        )
        file_selections.append(selection)
    return file_selections


def _get_default_file_size():
    return {"numFiles": 1, "numDirs": 1, "size": 1}
