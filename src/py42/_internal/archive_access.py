import posixpath
import time
from collections import namedtuple

from py42.exceptions import Py42ArchiveFileNotFoundError


FileSelection = namedtuple(u"FileSelection", u"path_set, num_files, num_dirs, size")


class FileType(object):
    DIRECTORY = u"directory"
    FILE = u"file"


class ArchiveAccessorManager(object):
    def __init__(self, archive_client, storage_client_factory):
        self._archive_client = archive_client
        self._storage_client_factory = storage_client_factory

    def get_archive_accessor(
        self,
        device_guid,
        destination_guid=None,
        private_password=None,
        encryption_key=None,
    ):
        client = self._storage_client_factory.from_device_guid(
            device_guid, destination_guid=destination_guid
        )
        decryption_keys = self._get_decryption_keys(
            device_guid, private_password, encryption_key
        )
        session_id = self._create_restore_session(
            client.archive, device_guid, **decryption_keys
        )
        restore_job_manager = create_restore_job_manager(
            client.archive, device_guid, session_id
        )
        file_size_poller = create_file_size_poller(client.archive, device_guid)
        return ArchiveAccessor(
            device_guid,
            session_id,
            client.archive,
            restore_job_manager,
            file_size_poller,
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
        return self._archive_client.get_data_key_token(device_guid)[u"dataKeyToken"]

    @staticmethod
    def _create_restore_session(storage_archive_client, device_guid, **kwargs):
        response = storage_archive_client.create_restore_session(device_guid, **kwargs)
        return response[u"webRestoreSessionId"]


def _create_file_selections(file_paths, metadata_list, file_sizes=None):
    file_selections = []
    for i in range(0, len(file_paths)):
        metadata = metadata_list[i]
        size_info = file_sizes[i] if file_sizes else _get_default_file_size()
        path_set = {
            u"type": metadata[u"type"],
            u"path": metadata[u"path"],
            u"selected": True,
        }
        selection = FileSelection(
            path_set, size_info[u"numFiles"], size_info[u"numDirs"], size_info[u"size"],
        )
        file_selections.append(selection)

    return file_selections


class ArchiveAccessor(object):

    DEFAULT_DIRECTORY_DOWNLOAD_NAME = u"download"
    JOB_POLLING_INTERVAL = 1

    def __init__(
        self,
        device_guid,
        archive_session_id,
        storage_archive_client,
        restore_job_manager,
        file_size_poller,
    ):
        self._device_guid = device_guid
        self._archive_session_id = archive_session_id
        self._storage_archive_client = storage_archive_client
        self._restore_job_manager = restore_job_manager
        self._file_size_poller = file_size_poller

    def stream_from_backup(self, file_paths, file_size_calc_timeout=None):
        if not isinstance(file_paths, (list, tuple)):
            file_paths = [file_paths]
        file_paths = [fp.replace(u"\\", u"/") for fp in file_paths]
        metadata_list = self._get_restore_metadata(file_paths)
        file_ids = [md[u"id"] for md in metadata_list]
        file_sizes = self._file_size_poller.get_file_sizes(
            file_ids, timeout=file_size_calc_timeout
        )
        file_selections = _create_file_selections(file_paths, metadata_list, file_sizes)
        return self._restore_job_manager.get_stream(file_selections)

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

        response = self._get_children(node_id=None)
        for root in response:
            if root[u"path"].lower() == path_root.lower():
                return self._walk_tree(response, root, path_parts[1:])

        raise Py42ArchiveFileNotFoundError(response, self._device_guid, file_path)

    def _walk_tree(self, response, current_node, remaining_path_components):
        if not remaining_path_components or not remaining_path_components[0]:
            return current_node

        children = self._get_children(node_id=current_node[u"id"])
        current_node_path = current_node[u"path"]
        target_child_path = posixpath.join(
            current_node_path, remaining_path_components[0]
        )

        for child in children:
            if child[u"path"].lower() == target_child_path.lower():
                return self._walk_tree(response, child, remaining_path_components[1:])

        raise Py42ArchiveFileNotFoundError(
            response, self._device_guid, target_child_path
        )

    def _get_children(self, node_id=None):
        return self._storage_archive_client.get_file_path_metadata(
            self._archive_session_id,
            self._device_guid,
            file_id=node_id,
            show_deleted=True,
        )


def _get_default_file_size():
    return {u"numFiles": 1, u"numDirs": 1, u"size": 1}


class _RestorePoller(object):
    JOB_POLLING_INTERVAL_SECONDS = 1

    def __init__(self, storage_archive_client, device_guid, job_polling_interval=None):
        self._storage_archive_client = storage_archive_client
        self._device_guid = device_guid
        self._job_polling_interval = (
            job_polling_interval or self.JOB_POLLING_INTERVAL_SECONDS
        )


class FileSizePoller(_RestorePoller):
    JOB_POLLING_TIMEOUT = 10

    def __init__(
        self, storage_archive_client, device_guid, job_polling_interval=None,
    ):
        super(FileSizePoller, self).__init__(
            storage_archive_client, device_guid, job_polling_interval
        )

    def get_file_sizes(self, file_ids, timeout=None):
        if timeout is None:
            timeout = self.JOB_POLLING_TIMEOUT

        # Allows a timeout of 0 to ignore file size calculation altogether
        if not timeout:
            return None

        sizes = []
        t0 = time.time()
        for file_id in file_ids:
            job_id = self.create_job(file_id)
            response = self.wait_for_job(job_id)
            sizes.append(
                {
                    u"numFiles": response[u"numFiles"],
                    u"numDirs": response[u"numDirs"],
                    u"size": response[u"size"],
                }
            )
            # File size calculation is taking too long.
            if time.time() - t0 > timeout:
                return None

        return sizes

    def create_job(self, file_id, timestamp=None, show_deleted=False):
        response = self._storage_archive_client.create_file_size_job(
            self._device_guid, file_id, timestamp, show_deleted
        )
        return response["jobId"]

    def wait_for_job(self, job_id):
        status = None
        response = None
        while status != u"DONE":
            response = self._storage_archive_client.get_file_size_job(
                job_id, self._device_guid
            )
            status = response[u"status"]
        return response

    def is_job_complete(self, job_id):
        response = self._storage_archive_client.get_file_size_job(
            job_id, self._device_guid
        )
        return self._get_completion_status(response) == u"DONE"

    @staticmethod
    def _get_completion_status(response):
        return response[u"status"]


class RestoreJobManager(_RestorePoller):
    def __init__(
        self,
        storage_archive_client,
        device_guid,
        archive_session_id,
        job_polling_interval=None,
    ):
        super(RestoreJobManager, self).__init__(
            storage_archive_client, device_guid, job_polling_interval
        )
        self._archive_session_id = archive_session_id

    def get_stream(self, file_selections):
        response = self._start_restore(file_selections)
        job_id = response["jobId"]
        while not self.is_job_complete(job_id):
            time.sleep(self._job_polling_interval)
        return self._get_stream(job_id)

    def is_job_complete(self, job_id):
        response = self._storage_archive_client.get_restore_status(job_id)
        return self._get_completion_status(response)

    def _start_restore(self, file_selection):
        num_files = sum([fs.num_files for fs in file_selection])
        num_dirs = sum([fs.num_dirs for fs in file_selection])
        size = sum([fs.size for fs in file_selection])
        zip_result = _check_for_multiple_files(file_selection) or None
        return self._storage_archive_client.start_restore(
            guid=self._device_guid,
            web_restore_session_id=self._archive_session_id,
            path_set=[fs.path_set for fs in file_selection],
            num_files=num_files,
            num_dirs=num_dirs,
            size=size,
            zip_result=zip_result,
            show_deleted=True,
        )

    @staticmethod
    def _get_completion_status(response):
        return response[u"done"]

    def _get_stream(self, job_id):
        response = self._storage_archive_client.stream_restore_result(job_id)
        return response


def create_restore_job_manager(storage_archive_client, device_guid, archive_session_id):
    return RestoreJobManager(storage_archive_client, device_guid, archive_session_id)


def create_file_size_poller(storage_archive_client, device_guid):
    return FileSizePoller(storage_archive_client, device_guid)


def _check_for_multiple_files(file_selection):
    if not file_selection:
        return False
    if len(file_selection) > 1:
        return True

    # Only one file selected
    selection = file_selection[0]
    return selection.path_set[u"type"].lower() == u"directory"
