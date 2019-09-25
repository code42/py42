# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

import py42
from py42._internal.compat import str
from py42._internal.file_event_filter import FilterGroup
from py42.sdk.file_event_query import (
    DeviceUsername,
    EventTimestamp,
    EventType,
    ExposureType,
    FileEventQuery,
    FileName,
    FilePath,
    MD5,
    OSHostname,
    PrivateIPAddress,
    PublicIPAddress,
    SHA256,
)

JSON_QUERY_BASE = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(group_clause, group_list, 1, 100, "asc", "eventId")


def test_file_event_query_constructs_successfully(event_filter_group):
    assert FileEventQuery(event_filter_group)


def test_file_event_query_str_with_single_filter_gives_correct_json_representation(
    event_filter_group
):
    file_event_query = FileEventQuery(event_filter_group)
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_unicode_with_single_filter_gives_correct_json_representation(
    unicode_event_filter_group
):
    file_event_query = FileEventQuery(unicode_event_filter_group)
    json_query_str = build_query_json("AND", unicode_event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_single_filter_and_specified_gives_correct_json_representation(
    event_filter_group
):
    file_event_query = FileEventQuery(event_filter_group, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_single_filter_or_specified_gives_correct_json_representation(
    event_filter_group
):
    file_event_query = FileEventQuery(event_filter_group, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_gives_correct_json_representation(
    event_filter_group_list
):
    file_event_query = FileEventQuery(event_filter_group_list)
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_and_specified_gives_correct_json_representation(
    event_filter_group_list
):
    file_event_query = FileEventQuery(event_filter_group_list, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_or_specified_gives_correct_json_representation(
    event_filter_group_list
):
    file_event_query = FileEventQuery(event_filter_group_list, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_num_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_number = 5
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 5, 100, "asc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_size_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_size = 500
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 500, "asc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_direction_gives_correct_json_representation(
    event_filter_group
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_direction = "desc"
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 100, "desc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_key_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 100, "asc", "some_field_to_sort_by"
    )
    assert str(file_event_query) == json_query_str


def test_md5_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    MD5.eq("test_md5")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "md5Checksum", "test_md5"
    )


def test_md5_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    MD5.not_eq("test_md5")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "md5Checksum", "test_md5"
    )


def test_md5_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["md51", "md52", "md53"]
    MD5.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "md5Checksum", items
    )


def test_md5_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["md51", "md52", "md53"]
    MD5.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "md5Checksum", items
    )


def test_sha256_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    SHA256.eq("test_sha256")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "sha256Checksum", "test_sha256"
    )


def test_sha256_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    SHA256.not_eq("test_sha256")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "sha256Checksum", "test_sha256"
    )


def test_sha256_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["sha2561", "sha2562", "sha2563"]
    SHA256.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "sha256Checksum", items
    )


def test_sha256_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["sha2561", "sha2562", "sha2563"]
    SHA256.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "sha256Checksum", items
    )


def test_os_hostname_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    OSHostname.eq("test_osHostName")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "osHostName", "test_osHostName"
    )


def test_os_hostname_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    OSHostname.not_eq("test_osHostName")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "osHostName", "test_osHostName"
    )


def test_os_hostname_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["osHostName1", "osHostName2", "osHostName3"]
    OSHostname.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "osHostName", items
    )


def test_os_hostname_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["osHostName1", "osHostName2", "osHostName3"]
    OSHostname.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "osHostName", items
    )


def test_device_username_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    DeviceUsername.eq("test_deviceUserName")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "deviceUserName", "test_deviceUserName"
    )


def test_device_username_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    DeviceUsername.not_eq("test_deviceUsername")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "deviceUserName", "test_deviceUsername"
    )


def test_device_username_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    DeviceUsername.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "deviceUserName", items
    )


def test_device_username_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    DeviceUsername.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "deviceUserName", items
    )


def test_unicode_device_username_eq_sets_filter_properties_correctly(mocker):
    unicode_username = "我能吞下玻璃而不伤身体"
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    DeviceUsername.eq(unicode_username)
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "deviceUserName", unicode_username
    )


def test_file_name_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    FileName.eq("test_fileName")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "fileName", "test_fileName"
    )


def test_file_name_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    FileName.not_eq("test_fileName")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "fileName", "test_fileName"
    )


def test_file_name_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["fileName", "fileName", "fileName"]
    FileName.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "fileName", items
    )


def test_file_name_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["fileName1", "fileName2", "fileName3"]
    FileName.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "fileName", items
    )


def test_file_path_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    FilePath.eq("test_filePath")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "filePath", "test_filePath"
    )


def test_file_path_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    FilePath.not_eq("test_filePath")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "filePath", "test_filePath"
    )


def test_file_path_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["filePath1", "filePath2", "filePath3"]
    FilePath.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "filePath", items
    )


def test_file_path_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["filePath1", "filePath2", "filePath3"]
    FilePath.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "filePath", items
    )


def test_public_ip_address_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    PublicIPAddress.eq("test_publicIp")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "publicIpAddress", "test_publicIp"
    )


def test_public_ip_address_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    PublicIPAddress.not_eq("test_publicIp")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "publicIpAddress", "test_publicIp"
    )


def test_public_ip_address_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    PublicIPAddress.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "publicIpAddress", items
    )


def test_public_ip_address_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    PublicIPAddress.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "publicIpAddress", items
    )


def test_private_ip_address_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    PrivateIPAddress.eq("test_privateIp")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "privateIpAddresses", "test_privateIp"
    )


def test_private_ip_address_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    PrivateIPAddress.not_eq("test_privateIp")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "privateIpAddresses", "test_privateIp"
    )


def test_private_ip_address_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["privateIp1", "privateIp2", "privateIp3"]
    PrivateIPAddress.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "privateIpAddresses", items
    )


def test_private_ip_address_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["privateIp1", "privateIp2", "privateIp3"]
    PrivateIPAddress.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "privateIpAddresses", items
    )


def test_event_type_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    EventType.eq("test_eventType")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "eventType", "test_eventType"
    )


def test_event_type_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    EventType.not_eq("test_eventType")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "eventType", "test_eventType"
    )


def test_event_type_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["eventType1", "eventType2", "eventType3"]
    EventType.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "eventType", items
    )


def test_event_type_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["eventType1", "eventType2", "eventType3"]
    EventType.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "eventType", items
    )


def test_exposure_type_any_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = [
        str(ExposureType.SHARED_VIA_LINK),
        str(ExposureType.SHARED_TO_DOMAIN),
        str(ExposureType.APPLICATION_READ),
        str(ExposureType.CLOUD_STORAGE),
        str(ExposureType.REMOVABLE_MEDIA),
        str(ExposureType.IS_PUBLIC),
    ]
    ExposureType.any()
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "exposure", items
    )


def test_exposure_type_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_eq_filter_group")
    ExposureType.eq("test_exposure")
    py42._internal.file_event_filter.create_eq_filter_group.assert_called_once_with(
        "exposure", "test_exposure"
    )


def test_exposure_type_not_eq_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_eq_filter_group")
    ExposureType.not_eq("test_exposure")
    py42._internal.file_event_filter.create_not_eq_filter_group.assert_called_once_with(
        "exposure", "test_exposure"
    )


def test_exposure_type_is_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_is_in_filter_group")
    items = ["exposure1", "exposure2", "exposure3"]
    ExposureType.is_in(items)
    py42._internal.file_event_filter.create_is_in_filter_group.assert_called_once_with(
        "exposure", items
    )


def test_exposure_type_not_in_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_not_in_filter_group")
    items = ["exposure1", "exposure2", "exposure3"]
    ExposureType.not_in(items)
    py42._internal.file_event_filter.create_not_in_filter_group.assert_called_once_with(
        "exposure", items
    )


def test_event_timestamp_on_or_after_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_on_or_after_filter_group")
    test_time = time()
    formatted = datetime.fromtimestamp(test_time).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    EventTimestamp.on_or_after(test_time)
    py42._internal.file_event_filter.create_on_or_after_filter_group.assert_called_once_with(
        "eventTimestamp", formatted
    )


def test_event_timestamp_on_or_before_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_on_or_before_filter_group")
    test_time = time()
    formatted = datetime.fromtimestamp(test_time).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    EventTimestamp.on_or_before(test_time)
    py42._internal.file_event_filter.create_on_or_before_filter_group.assert_called_once_with(
        "eventTimestamp", formatted
    )


def test_event_timestamp_in_range_sets_filter_properties_correctly(mocker):
    mocker.patch("py42._internal.file_event_filter.create_in_range_filter_group")
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = datetime.fromtimestamp(test_before_time).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    formatted_after = datetime.fromtimestamp(test_after_time).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    EventTimestamp.in_range(test_before_time, test_after_time)
    py42._internal.file_event_filter.create_in_range_filter_group.assert_called_once_with(
        "eventTimestamp", formatted_before, formatted_after
    )
