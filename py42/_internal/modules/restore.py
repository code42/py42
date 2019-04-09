import os
import posixpath
import time

from collections import namedtuple

import py42.util as util
from py42._internal.clients.archive import ArchiveClient
from py42._internal.clients.restore import RestoreClient
from py42._internal.storage_client_factory import StorageClientFactory


class RestoreModule(object):

    def __init__(self, restore_client, storage_client_factory, downloader):
        # type: (RestoreClient, StorageClientFactory, FileDownloader) -> None
        self._restore_client = restore_client
        self._storage_client_factory = storage_client_factory
        self._downloader = downloader

    def get_restore_history(self, days, org_id=None, page_num=None, page_size=None, **kwargs):
        self._restore_client.get_restore_history(days, org_id=org_id, page_num=page_num, page_size=page_size, **kwargs)

    def get_web_restore_info(self, src_guid, dest_guid, **kwargs):
        self._restore_client.get_web_restore_info(src_guid, dest_guid, **kwargs)

    def download_from_backup(self, file_path, device_guid, destination_guid=None, save_as_dir=None,
                             save_as_filename=None):
        return self._downloader.download_file(file_path, device_guid, destination_guid, save_as_dir, save_as_filename)


class FileDownloader(object):
    JOB_POLLING_INTERVAL = 1

    def __init__(self, archive_client, storage_client_factory):
        # type: (ArchiveClient, StorageClientFactory) -> None
        self._archive = archive_client
        self._storage_client_factory = storage_client_factory

    def download_file(self, file_path, device_guid, destination_guid=None, save_as_dir=None, save_as_filename=None):
        save_as_dir = _get_save_as_dir(save_as_dir)
        return self._download_file_by_path(device_guid, destination_guid, file_path, save_as_dir, save_as_filename)

    def _download_file_by_path(self, device_guid, dest_guid, file_path, save_as_dir, save_as_filename):
        data_key_token = self._get_data_key_token(device_guid)

        storage_client = self._storage_client_factory.create_backup_client(device_guid=device_guid,
                                                                           destination_guid=dest_guid)

        return self._restore_file(storage_client, device_guid, data_key_token, file_path, save_as_dir,
                                  save_as_filename)

    def _restore_file(self, storage_client, device_guid, data_key_token, file_path, save_as_dir,
                      save_as_filename):

        session_id = self._create_web_restore_session(storage_client.restore, device_guid, data_key_token)

        file_selection = self._build_file_selection(storage_client.archive, session_id, device_guid,
                                                    file_path)

        save_as_path = _get_writeable_save_as_path(save_as_dir, _get_filename(file_selection), save_as_filename)

        job_id = self._submit_web_restore_job(storage_client.restore, device_guid, session_id, file_selection)

        while not self._get_web_restore_job(storage_client.restore, job_id)['done']:
            time.sleep(FileDownloader.JOB_POLLING_INTERVAL)

        self._download_result(storage_client.restore, job_id, save_as_path)

        return save_as_path

    @staticmethod
    def _create_web_restore_session(restore_client, device_guid, data_key_token):
        response = restore_client.create_web_restore_session(device_guid, data_key_token=data_key_token)
        return util.get_obj_from_response(response, 'data')['webRestoreSessionId']

    @staticmethod
    def _submit_web_restore_job(restore_client, device_guid, web_restore_session_id, file_selection):
        response = restore_client.submit_web_restore_job(device_guid, web_restore_session_id, file_selection.path_set,
                                                         file_selection.num_files, file_selection.num_dirs,
                                                         file_selection.size)
        return util.get_obj_from_response(response, 'data')['jobId']

    @staticmethod
    def _get_web_restore_job(restore_client, job_id):
        response = restore_client.get_web_restore_job(job_id)
        return util.get_obj_from_response(response, 'data')

    @staticmethod
    def _download_result(restore_client, job_id, filename):
        response = restore_client.get_web_restore_job_result(job_id, stream=True)
        with open(filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

    def _build_file_selection(self, archive_client, session_id, device_guid, file_path):
        file_metadata = self._get_metadata_for_file(archive_client, session_id, device_guid, file_path)
        file_size_data = self._get_file_size(archive_client, device_guid, file_metadata['id'])
        return _to_file_selection(file_metadata, file_size_data)

    def _get_metadata_for_file(self, archive_client, session_id, device_guid, file_path):
        file_metadata = self._get_file_via_walking_tree(archive_client, session_id, device_guid, file_path)
        if not file_metadata:
            raise Exception("File not found in archive for device {0} at path {1}"
                            .format(device_guid, file_path))
        return file_metadata

    def _get_file_via_walking_tree(self, archive_client, session_id, device_guid, file_path):
        path_parts = file_path.split("/")
        drive = self._get_drive(archive_client, session_id, device_guid, path_parts[0] + "/")
        return self._walk_tree(archive_client, session_id, device_guid, drive, path_parts[1:])

    def _get_drive(self, archive_client, session_id, device_guid, drive_name):
        drives = self._get_children(archive_client, session_id, device_guid)
        for drive in drives:
            if drive["path"] == drive_name:
                return drive

    def _walk_tree(self, archive_client, session_id, device_guid, current_node, remaining_path_components):

        if len(remaining_path_components) == 0:
            return current_node
        elif len(remaining_path_components[0]) == 0:
            return current_node

        children = self._get_children(archive_client, session_id, device_guid, current_node["id"])

        current_node_path = current_node["path"]

        # drive paths don't end with a '/'
        if not current_node_path[-1] == "/":
            current_node_path += "/"

        target_child = str(current_node_path + remaining_path_components[0]).lower()

        for child in children:
            if child["path"].lower() == target_child:
                return self._walk_tree(archive_client, session_id, device_guid, child, remaining_path_components[1:])

        return None

    @staticmethod
    def _get_children(archive_client, session_id, device_guid, node_id=None):
        children_response = archive_client.get_archive_tree_node(session_id, device_guid, node_id)
        return util.get_obj_from_response(children_response, 'data')

    @staticmethod
    def _get_file_size(archive_client, device_guid, file_id):
        response = archive_client.get_file_size(device_guid, file_id)
        return util.get_obj_from_response(response, 'data')

    def _get_data_key_token(self, device_guid):
        response = self._archive.get_data_key_token(device_guid)
        return util.get_obj_from_response(response, 'dataKeyToken')


FileSelection = namedtuple('FileSelection', 'path_set, num_files, num_dirs, size')


def _get_save_as_dir(save_as_dir=None):
    if not save_as_dir:
        save_as_dir = posixpath.curdir
    if not posixpath.exists(save_as_dir):
        raise Exception("Save-as directory does not exist: {0}".format(save_as_dir))
    return save_as_dir


def _get_writeable_save_as_path(save_as_dir, filename, save_as_filename):
    save_as_path = _get_save_as_path(save_as_dir, filename, save_as_filename)
    _verify_write_permissions(save_as_path)
    return save_as_path


def _get_save_as_path(save_as_dir, filename, save_as_filename=None):
    if not save_as_filename:
        save_as_filename = filename
    return posixpath.join(save_as_dir, save_as_filename)


def _get_filename(file_selection):
    path = file_selection.path_set[0]["path"]
    name = posixpath.basename(path)
    if file_selection.path_set[0]["type"] == "directory":
        if len(name) == 0:
            name = "download"
        name += ".zip"
    return name


def _to_file_selection(file_metadata, file_size_data):
    path_set = [{"type": file_metadata["type"], "path": file_metadata['path'], "selected": True}]
    num_files = file_size_data['numFiles']
    num_dirs = file_size_data['numDirs']
    size = file_size_data['size']
    return FileSelection(path_set, num_files, num_dirs, size)


def _verify_write_permissions(save_as_path):
    # If the file exists, see if we can overwrite it.
    if posixpath.exists(save_as_path):
        if not os.access(save_as_path, os.W_OK):
            raise Exception("Insufficient permissions to write to file: {0}".format(save_as_path))
    else:
        # Otherwise see if we can write to the directory (assuming it already exists)
        directory = posixpath.dirname(save_as_path)
        if not posixpath.exists(directory):
            raise Exception("Directory does not exist: {0}".format(directory))
        if not os.access(directory, os.W_OK):
            raise Exception("Insufficient permissions to write to directory: {0}".format(directory))
