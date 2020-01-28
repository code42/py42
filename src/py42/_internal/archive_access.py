import posixpath
import time
from collections import namedtuple

import py42.util as util
from py42._internal.client_factories import StorageClientFactory
from py42._internal.clients.archive import ArchiveClient

FileSelection = namedtuple(u"FileSelection", u"path_set, num_files, num_dirs, size")


class FileType(object):
    DIRECTORY = u"directory"
    FILE = u"file"


class ArchiveAccessorManager(object):
    def __init__(self, archive_client, storage_client_factory):
        # type: (ArchiveClient, StorageClientFactory) -> None
        self._archive_client = archive_client
        self._storage_client_factory = storage_client_factory

    def get_archive_accessor(self, device_guid, destination_guid=None):
        client = self._storage_client_factory.get_storage_client_from_device_guid(
            device_guid, destination_guid=destination_guid
        )
        data_key_token = self._get_data_key_token(device_guid)
        session_id = self._create_web_restore_session(client.archive, device_guid, data_key_token)
        restore_job_manager = create_restore_job_manager(client.archive, device_guid, session_id)
        return ArchiveAccessor(device_guid, session_id, client.archive, restore_job_manager)

    def _get_data_key_token(self, device_guid):
        response = self._archive_client.get_data_key_token(device_guid)
        return util.get_obj_from_response(response, u"dataKeyToken")

    @staticmethod
    def _create_web_restore_session(storage_archive_client, device_guid, data_key_token):
        response = storage_archive_client.create_web_restore_session(
            device_guid, data_key_token=data_key_token
        )
        return util.get_obj_from_response(response, u"webRestoreSessionId")


class ArchiveAccessor(object):

    DEFAULT_DIRECTORY_DOWNLOAD_NAME = u"download"
    JOB_POLLING_INTERVAL = 1

    def __init__(
        self, device_guid, archive_session_id, storage_archive_client, restore_job_manager
    ):
        self._device_guid = device_guid
        self._archive_session_id = archive_session_id
        self._storage_archive_client = storage_archive_client
        self._restore_job_manager = restore_job_manager

    def download_from_backup(
        self, file_path, save_as_dir=None, save_as_filename=None, then=None, **kwargs
    ):
        def handle_file_metadata(metadata):
            file_selection = self._build_file_selection(metadata[u"path"], metadata[u"type"])

            # get and verify we can write to the save-as path before attempting to download the file
            filename = save_as_filename or get_download_filename(
                metadata[u"path"], metadata[u"type"]
            )
            save_as_path = util.build_path(filename, directory=save_as_dir)
            save_as_path = util.verify_path_writeable(save_as_path)

            return self._restore_job_manager.restore_to_local_path(
                file_selection, save_as_path, then=then
            )

        return self._get_file_via_walking_tree(file_path, then=handle_file_metadata, **kwargs)

    def _get_file_via_walking_tree(self, file_path, then=None, **kwargs):
        path_parts = file_path.split("/")
        path_root = path_parts[0] + "/"

        def handle_archive_roots(response):
            roots = util.get_obj_from_response(response, u"data")
            for root in roots:
                if root["path"].lower() == path_root.lower():
                    return self._walk_tree(root, path_parts[1:], then=then, **kwargs)

            raise Exception(
                u"File not found in archive for device {0} at path {1}".format(
                    self._device_guid, file_path
                )
            )

        return self._get_children(then=handle_archive_roots, node_id=None)

    def _walk_tree(self, current_node, remaining_path_components, then=None, **kwargs):
        if not remaining_path_components or not remaining_path_components[0]:
            return then(current_node)

        def handle_get_children(response):
            children = util.get_obj_from_response(response, u"data")
            current_node_path = current_node[u"path"]
            target_child_path = posixpath.join(current_node_path, remaining_path_components[0])

            for child in children:
                if child[u"path"].lower() == target_child_path.lower():
                    return self._walk_tree(
                        child, remaining_path_components[1:], then=then, **kwargs
                    )

            raise Exception(
                u"File not found in archive for device {0} at path {1}".format(
                    self._device_guid, target_child_path
                )
            )

        return self._get_children(then=handle_get_children, node_id=current_node[u"id"], **kwargs)

    def _get_children(self, then=None, node_id=None, **kwargs):
        return self._storage_archive_client.get_archive_tree_node(
            self._archive_session_id,
            self._device_guid,
            file_id=node_id,
            show_deleted=True,
            then=then,
            **kwargs
        )

    @staticmethod
    def _build_file_selection(file_path, file_type):
        path_set = [{u"type": file_type, u"path": file_path, u"selected": True}]
        # pass in dummy values; only used with progress indication, which we don't currently use
        num_files = num_dirs = size = 1
        return FileSelection(path_set, num_files, num_dirs, size)


class RestoreJobManager(object):

    JOB_POLLING_INTERVAL_SECONDS = 1

    def __init__(
        self,
        storage_archive_client,
        device_guid,
        archive_session_id,
        job_polling_interval=JOB_POLLING_INTERVAL_SECONDS,
    ):
        self._storage_archive_client = storage_archive_client
        self._device_guid = device_guid
        self._archive_session_id = archive_session_id
        self._job_polling_interval = job_polling_interval

    def restore_to_local_path(self, file_selection, save_as_path, then=None, **kwargs):
        def do_download(response):
            job_id = util.get_obj_from_response(response, u"jobId")
            while not self.is_job_complete(job_id):
                time.sleep(self._job_polling_interval)
            return self._download_result(job_id, save_as_path, then=then)

        return self._submit_web_restore_job(file_selection, then=do_download, **kwargs)

    def is_job_complete(self, job_id, **kwargs):
        response = self._storage_archive_client.get_web_restore_job(job_id, **kwargs)
        return self._get_completion_status(response)

    def _submit_web_restore_job(self, file_selection, then=None, **kwargs):
        return self._storage_archive_client.submit_web_restore_job(
            self._device_guid,
            self._archive_session_id,
            file_selection.path_set,
            file_selection.num_files,
            file_selection.num_dirs,
            file_selection.size,
            show_deleted=True,
            then=then,
            **kwargs
        )

    @staticmethod
    def _get_completion_status(response):
        return util.get_obj_from_response(response, u"done")

    def _download_result(self, job_id, file_path, then=None, **kwargs):
        def write_file(response):
            util.save_content_to_disk(response, file_path)

            if then:
                then(file_path)
            return file_path

        return self._storage_archive_client.get_web_restore_job_result(
            job_id, stream=True, then=write_file, **kwargs
        )


def get_download_filename(file_path, file_type, default_dir_name=u"download"):
    # directory file paths should not end with a '/'. If they do, the name will be interpreted as an empty string,
    # and "download.zip" will be used. Paths from the archive, which are currently the only paths passed to this
    # method, do not have trailing slashes.
    name = posixpath.basename(file_path)
    if file_type == FileType.DIRECTORY:
        if not name:
            name = default_dir_name
        name += u".zip"
    return name


def create_restore_job_manager(storage_archive_client, device_guid, archive_session_id):
    return RestoreJobManager(storage_archive_client, device_guid, archive_session_id)
