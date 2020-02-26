# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

from .conftest import (
    format_timestamp,
    format_datetime,
    EXISTS,
    NOT_EXISTS,
    IS,
    IS_NOT,
    IS_IN,
    NOT_IN,
    ON_OR_AFTER,
    ON_OR_BEFORE,
    IN_RANGE,
    CONTAINS,
    NOT_CONTAINS,
)
from py42._internal.compat import str
from py42.sdk.file_event_query import (
    Actor,
    DeviceUsername,
    EventTimestamp,
    EventType,
    ExposureType,
    FileEventQuery,
    FileName,
    FilePath,
    InsertionTimestamp,
    MD5,
    OSHostname,
    PrivateIPAddress,
    ProcessName,
    ProcessOwner,
    PublicIPAddress,
    SHA256,
    SharedWith,
    Source,
    TabURL,
    Shared,
    RemovableMediaName,
    FileOwner,
)

JSON_QUERY_BASE = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(group_clause, group_list, 1, 10000, "asc", "eventId")


def test_file_event_query_repr_does_not_throw_type_error():
    # On python 2, `repr` doesn't throw.
    # On python 3, if `repr` doesn't return type `str`, then an exception is thrown.
    try:
        _ = repr(FileEventQuery())
    except TypeError:
        assert False


def test_file_event_query_constructs_successfully(event_filter_group):
    assert FileEventQuery(event_filter_group)


def test_file_event_query_str_with_single_filter_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_unicode_with_single_filter_gives_correct_json_representation(
    unicode_event_filter_group,
):
    file_event_query = FileEventQuery(unicode_event_filter_group)
    json_query_str = build_query_json("AND", unicode_event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_single_filter_and_specified_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_single_filter_or_specified_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_gives_correct_json_representation(
    event_filter_group_list,
):
    file_event_query = FileEventQuery(event_filter_group_list)
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_and_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    file_event_query = FileEventQuery(event_filter_group_list, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_or_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    file_event_query = FileEventQuery(event_filter_group_list, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_num_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_number = 5
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 5, 10000, "asc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_size_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_size = 500
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 500, "asc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_direction_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_direction = "desc"
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 10000, "desc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_key_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 10000, "asc", "some_field_to_sort_by"
    )
    assert str(file_event_query) == json_query_str


def test_actor_exists_str_gives_correct_json_representation():
    _filter = Actor.exists()
    expected = EXISTS.format("actor")
    assert str(_filter) == expected


def test_actor_not_exists_str_gives_correct_json_representation():
    _filter = Actor.not_exists()
    expected = NOT_EXISTS.format("actor")
    assert str(_filter) == expected


def test_actor_eq_str_gives_correct_json_representation():
    _filter = Actor.eq("test_actor")
    expected = IS.format("actor", "test_actor")
    assert str(_filter) == expected


def test_actor_not_eq_str_gives_correct_json_representation():
    _filter = Actor.not_eq("test_actor")
    expected = IS_NOT.format("actor", "test_actor")
    assert str(_filter) == expected


def test_actor_is_in_str_gives_correct_json_representation():
    items = ["actor1", "actor2", "actor3"]
    _filter = Actor.is_in(items)
    expected = IS_IN.format("actor", *items)
    assert str(_filter) == expected


def test_actor_not_in_str_gives_correct_json_representation():
    items = ["actor1", "actor2", "actor3"]
    _filter = Actor.not_in(items)
    expected = NOT_IN.format("actor", *items)
    assert str(_filter) == expected


def test_device_username_exists_str_gives_correct_json_representation():
    _filter = DeviceUsername.exists()
    expected = EXISTS.format("deviceUserName")
    assert str(_filter) == expected


def test_device_username_not_exists_str_gives_correct_json_representation():
    _filter = DeviceUsername.not_exists()
    expected = NOT_EXISTS.format("deviceUserName")
    assert str(_filter) == expected


def test_device_username_eq_str_gives_correct_json_representation():
    _filter = DeviceUsername.eq("test_deviceUserName")
    expected = IS.format("deviceUserName", "test_deviceUserName")
    assert str(_filter) == expected


def test_device_username_not_eq_str_gives_correct_json_representation():
    _filter = DeviceUsername.not_eq("test_deviceUserName")
    expected = IS_NOT.format("deviceUserName", "test_deviceUserName")
    assert str(_filter) == expected


def test_device_username_is_in_str_gives_correct_json_representation():
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    _filter = DeviceUsername.is_in(items)
    expected = IS_IN.format("deviceUserName", *items)
    assert str(_filter) == expected


def test_device_username_not_in_str_gives_correct_json_representation():
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    _filter = DeviceUsername.not_in(items)
    expected = NOT_IN.format("deviceUserName", *items)
    assert str(_filter) == expected


def test_device_username_eq_unicode_str_gives_correct_json_representation():
    unicode_username = u"您已经发现了秘密信息"
    _filter = DeviceUsername.eq(unicode_username)
    expected = IS.format(
        u"deviceUserName", u"\u60a8\u5df2\u7ecf\u53d1\u73b0\u4e86\u79d8\u5bc6\u4fe1\u606f"
    )
    assert str(_filter) == expected


def test_event_timestamp_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = EventTimestamp.on_or_after(test_time)
    expected = ON_OR_AFTER.format("eventTimestamp", formatted)
    assert str(_filter) == expected


def test_event_timestamp_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = EventTimestamp.on_or_before(test_time)
    expected = ON_OR_BEFORE.format("eventTimestamp", formatted)
    assert str(_filter) == expected


def test_event_timestamp_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = EventTimestamp.in_range(test_before_time, test_after_time)
    expected = IN_RANGE.format("eventTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_event_timestamp_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    _filter = EventTimestamp.on_same_day(test_time)
    expected = IN_RANGE.format("eventTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_event_type_exists_str_gives_correct_json_representation():
    _filter = EventType.exists()
    expected = EXISTS.format("eventType")
    assert str(_filter) == expected


def test_event_type_not_exists_str_gives_correct_json_representation():
    _filter = EventType.not_exists()
    expected = NOT_EXISTS.format("eventType")
    assert str(_filter) == expected


def test_event_type_eq_str_gives_correct_json_representation():
    _filter = EventType.eq("test_eventType")
    expected = IS.format("eventType", "test_eventType")
    assert str(_filter) == expected


def test_event_type_not_eq_str_gives_correct_json_representation():
    _filter = EventType.not_eq("test_eventType")
    expected = IS_NOT.format("eventType", "test_eventType")
    assert str(_filter) == expected


def test_event_type_is_in_str_gives_correct_json_representation():
    items = ["eventType1", "eventType2", "eventType3"]
    _filter = EventType.is_in(items)
    expected = IS_IN.format("eventType", *items)
    assert str(_filter) == expected


def test_event_type_not_in_str_gives_correct_json_representation():
    items = ["eventType1", "eventType2", "eventType3"]
    _filter = EventType.not_in(items)
    expected = NOT_IN.format("eventType", *items)
    assert str(_filter) == expected


def test_exposure_type_exists_str_gives_correct_json_representation():
    _filter = ExposureType.exists()
    expected = EXISTS.format("exposure")
    assert str(_filter) == expected


def test_exposure_type_not_exists_str_gives_correct_json_representation():
    _filter = ExposureType.not_exists()
    expected = NOT_EXISTS.format("exposure")
    assert str(_filter) == expected


def test_exposure_type_eq_str_gives_correct_json_representation():
    _filter = ExposureType.eq("test_exposure")
    expected = IS.format("exposure", "test_exposure")
    assert str(_filter) == expected


def test_exposure_type_not_eq_str_gives_correct_json_representation():
    _filter = ExposureType.not_eq("test_exposure")
    expected = IS_NOT.format("exposure", "test_exposure")
    assert str(_filter) == expected


def test_exposure_type_is_in_str_gives_correct_json_representation():
    items = ["exposure1", "exposure2", "exposure3"]
    _filter = ExposureType.is_in(items)
    expected = IS_IN.format("exposure", *items)
    assert str(_filter) == expected


def test_exposure_type_not_in_str_gives_correct_json_representation():
    items = ["exposure1", "exposure2", "exposure3"]
    _filter = ExposureType.not_in(items)
    expected = NOT_IN.format("exposure", *items)
    assert str(_filter) == expected


def test_file_owner_exists_str_gives_correct_json_representation():
    _filter = FileOwner.exists()
    expected = EXISTS.format("fileOwner")
    assert str(_filter) == expected


def test_file_owner_not_exists_str_gives_correct_json_representation():
    _filter = FileOwner.not_exists()
    expected = NOT_EXISTS.format("fileOwner")
    assert str(_filter) == expected


def test_file_owner_eq_str_gives_correct_json_representation():
    _filter = FileOwner.eq("test_fileName")
    expected = IS.format("fileOwner", "test_fileName")
    assert str(_filter) == expected


def test_file_owner_not_eq_str_gives_correct_json_representation():
    _filter = FileOwner.not_eq("test_fileName")
    expected = IS_NOT.format("fileOwner", "test_fileName")
    assert str(_filter) == expected


def test_file_owner_is_in_str_gives_correct_json_representation():
    items = ["fileOwner1", "fileOwner2", "fileOwner3"]
    _filter = FileOwner.is_in(items)
    expected = IS_IN.format("fileOwner", *items)
    assert str(_filter) == expected


def test_file_owner_not_in_str_gives_correct_json_representation():
    items = ["fileOwner1", "fileOwner2", "fileOwner3"]
    _filter = FileOwner.not_in(items)
    expected = NOT_IN.format("fileOwner", *items)
    assert str(_filter) == expected


def test_file_name_exists_str_gives_correct_json_representation():
    _filter = FileName.exists()
    expected = EXISTS.format("fileName")
    assert str(_filter) == expected


def test_file_name_not_exists_str_gives_correct_json_representation():
    _filter = FileName.not_exists()
    expected = NOT_EXISTS.format("fileName")
    assert str(_filter) == expected


def test_file_name_eq_str_gives_correct_json_representation():
    _filter = FileName.eq("test_fileName")
    expected = IS.format("fileName", "test_fileName")
    assert str(_filter) == expected


def test_file_name_not_eq_str_gives_correct_json_representation():
    _filter = FileName.not_eq("test_fileName")
    expected = IS_NOT.format("fileName", "test_fileName")
    assert str(_filter) == expected


def test_file_name_is_in_str_gives_correct_json_representation():
    items = ["fileName", "fileName", "fileName"]
    _filter = FileName.is_in(items)
    expected = IS_IN.format("fileName", *items)
    assert str(_filter) == expected


def test_file_name_not_in_str_gives_correct_json_representation():
    items = ["fileName1", "fileName2", "fileName3"]
    _filter = FileName.not_in(items)
    expected = NOT_IN.format("fileName", *items)
    assert str(_filter) == expected


def test_file_path_exists_str_gives_correct_json_representation():
    _filter = FilePath.exists()
    expected = EXISTS.format("filePath")
    assert str(_filter) == expected


def test_file_path_not_exists_str_gives_correct_json_representation():
    _filter = FilePath.not_exists()
    expected = NOT_EXISTS.format("filePath")
    assert str(_filter) == expected


def test_file_path_eq_str_gives_correct_json_representation():
    _filter = FilePath.eq("test_filePath")
    expected = IS.format("filePath", "test_filePath")
    assert str(_filter) == expected


def test_file_path_not_eq_str_gives_correct_json_representation():
    _filter = FilePath.not_eq("test_filePath")
    expected = IS_NOT.format("filePath", "test_filePath")
    assert str(_filter) == expected


def test_file_path_is_in_str_gives_correct_json_representation():
    items = ["filePath1", "filePath2", "filePath3"]
    _filter = FilePath.is_in(items)
    expected = IS_IN.format("filePath", *items)
    assert str(_filter) == expected


def test_file_path_not_in_str_gives_correct_json_representation():
    items = ["filePath1", "filePath2", "filePath3"]
    _filter = FilePath.not_in(items)
    expected = NOT_IN.format("filePath", *items)
    assert str(_filter) == expected


def test_insertion_timestamp_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = InsertionTimestamp.on_or_after(test_time)
    expected = ON_OR_AFTER.format("insertionTimestamp", formatted)

    assert str(_filter) == expected


def test_insertion_timestamp_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = InsertionTimestamp.on_or_before(test_time)
    expected = ON_OR_BEFORE.format("insertionTimestamp", formatted)
    assert str(_filter) == expected


def test_insertion_timestamp_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = InsertionTimestamp.in_range(test_before_time, test_after_time)
    expected = IN_RANGE.format("insertionTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_insertion_timestamp_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)
    _filter = InsertionTimestamp.on_same_day(test_time)
    expected = IN_RANGE.format("insertionTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_md5_exists_str_gives_correct_json_representation():
    _filter = MD5.exists()
    expected = EXISTS.format("md5Checksum")
    assert str(_filter) == expected


def test_md5_not_exists_str_gives_correct_json_representation():
    _filter = MD5.not_exists()
    expected = NOT_EXISTS.format("md5Checksum")
    assert str(_filter) == expected


def test_md5_eq_str_gives_correct_json_representation():
    _filter = MD5.eq("test_md5")
    expected = IS.format("md5Checksum", "test_md5")
    assert str(_filter) == expected


def test_md5_not_eq_str_gives_correct_json_representation():
    _filter = MD5.not_eq("test_md5")
    expected = IS_NOT.format("md5Checksum", "test_md5")
    assert str(_filter) == expected


def test_md5_is_in_str_gives_correct_json_representation():
    items = ["md51", "md52", "md53"]
    _filter = MD5.is_in(items)
    expected = IS_IN.format("md5Checksum", *items)
    assert str(_filter) == expected


def test_md5_not_in_str_gives_correct_json_representation():
    items = ["md51", "md52", "md53"]
    _filter = MD5.not_in(items)
    expected = NOT_IN.format("md5Checksum", *items)
    assert str(_filter) == expected


def test_os_hostname_exists_str_gives_correct_json_representation():
    _filter = OSHostname.exists()
    expected = EXISTS.format("osHostName")
    assert str(_filter) == expected


def test_os_hostname_not_exists_str_gives_correct_json_representation():
    _filter = OSHostname.not_exists()
    expected = NOT_EXISTS.format("osHostName")
    assert str(_filter) == expected


def test_os_hostname_eq_str_gives_correct_json_representation():
    _filter = OSHostname.eq("test_osHostName")
    expected = IS.format("osHostName", "test_osHostName")
    assert str(_filter) == expected


def test_os_hostname_not_eq_str_gives_correct_json_representation():
    _filter = OSHostname.not_eq("test_osHostName")
    expected = IS_NOT.format("osHostName", "test_osHostName")
    assert str(_filter) == expected


def test_os_hostname_is_in_str_gives_correct_json_representation():
    items = ["osHostName1", "osHostName2", "osHostName3"]
    _filter = OSHostname.is_in(items)
    expected = IS_IN.format("osHostName", *items)
    assert str(_filter) == expected


def test_os_hostname_not_in_str_gives_correct_json_representation():
    items = ["osHostName1", "osHostName2", "osHostName3"]
    _filter = OSHostname.not_in(items)
    expected = NOT_IN.format("osHostName", *items)
    assert str(_filter) == expected


def test_private_ip_exists_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.exists()
    expected = EXISTS.format("privateIpAddresses")
    assert str(_filter) == expected


def test_private_ip_not_exists_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.not_exists()
    expected = NOT_EXISTS.format("privateIpAddresses")
    assert str(_filter) == expected


def test_private_ip_address_eq_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.eq("test_privateIp")
    expected = IS.format("privateIpAddresses", "test_privateIp")
    assert str(_filter) == expected


def test_private_ip_address_not_eq_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.not_eq("test_privateIp")
    expected = IS_NOT.format("privateIpAddresses", "test_privateIp")
    assert str(_filter) == expected


def test_private_ip_address_is_in_str_gives_correct_json_representation():
    items = ["privateIp1", "privateIp2", "privateIp3"]
    _filter = PrivateIPAddress.is_in(items)
    expected = IS_IN.format("privateIpAddresses", *items)
    assert str(_filter) == expected


def test_private_ip_address_not_in_str_gives_correct_json_representation():
    items = ["privateIp1", "privateIp2", "privateIp3"]
    _filter = PrivateIPAddress.not_in(items)
    expected = NOT_IN.format("privateIpAddresses", *items)
    assert str(_filter) == expected


def test_process_owner_exists_str_gives_correct_json_representation():
    _filter = ProcessOwner.exists()
    expected = EXISTS.format("processOwner")
    assert str(_filter) == expected


def test_process_owner_not_exists_str_gives_correct_json_representation():
    _filter = ProcessOwner.not_exists()
    expected = NOT_EXISTS.format("processOwner")
    assert str(_filter) == expected


def test_process_owner_eq_str_gives_correct_json_representation():
    _filter = ProcessOwner.eq("test_owner")
    expected = IS.format("processOwner", "test_owner")
    assert str(_filter) == expected


def test_process_owner_not_eq_str_gives_correct_json_representation():
    _filter = ProcessOwner.not_eq("test_owner")
    expected = IS_NOT.format("processOwner", "test_owner")
    assert str(_filter) == expected


def test_process_owner_is_in_str_gives_correct_json_representation():
    items = ["owner1", "owner2", "owner3"]
    _filter = ProcessOwner.is_in(items)
    expected = IS_IN.format("processOwner", *items)
    assert str(_filter) == expected


def test_process_owner_not_in_str_gives_correct_json_representation():
    items = ["owner1", "owner2", "owner3"]
    _filter = ProcessOwner.not_in(items)
    expected = NOT_IN.format("processOwner", *items)
    assert str(_filter) == expected


def test_process_name_exists_str_gives_correct_json_representation():
    _filter = ProcessName.exists()
    expected = EXISTS.format("processName")
    assert str(_filter) == expected


def test_process_name_not_exists_str_gives_correct_json_representation():
    _filter = ProcessName.not_exists()
    expected = NOT_EXISTS.format("processName")
    assert str(_filter) == expected


def test_process_name_eq_str_gives_correct_json_representation():
    _filter = ProcessName.eq("test_name")
    expected = IS.format("processName", "test_name")
    assert str(_filter) == expected


def test_process_name_not_eq_str_gives_correct_json_representation():
    _filter = ProcessName.not_eq("test_name")
    expected = IS_NOT.format("processName", "test_name")
    assert str(_filter) == expected


def test_process_name_is_in_str_gives_correct_json_representation():
    items = ["n1", "n2", "n3"]
    _filter = ProcessName.is_in(items)
    expected = IS_IN.format("processName", *items)
    assert str(_filter) == expected


def test_process_name_not_in_str_gives_correct_json_representation():
    items = ["n1", "n2", "n3"]
    _filter = ProcessName.not_in(items)
    expected = NOT_IN.format("processName", *items)
    assert str(_filter) == expected


def test_public_ip_address_exists_str_gives_correct_json_representation():
    _filter = PublicIPAddress.exists()
    expected = EXISTS.format("publicIpAddress")
    assert str(_filter) == expected


def test_public_ip_address_not_exists_str_gives_correct_json_representation():
    _filter = PublicIPAddress.not_exists()
    expected = NOT_EXISTS.format("publicIpAddress")
    assert str(_filter) == expected


def test_public_ip_address_eq_str_gives_correct_json_representation():
    _filter = PublicIPAddress.eq("test_publicIp")
    expected = IS.format("publicIpAddress", "test_publicIp")
    assert str(_filter) == expected


def test_public_ip_address_not_eq_str_gives_correct_json_representation():
    _filter = PublicIPAddress.not_eq("test_publicIp")
    expected = IS_NOT.format("publicIpAddress", "test_publicIp")
    assert str(_filter) == expected


def test_public_ip_address_is_in_str_gives_correct_json_representation():
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    _filter = PublicIPAddress.is_in(items)
    expected = IS_IN.format("publicIpAddress", *items)
    assert str(_filter) == expected


def test_public_ip_address_not_in_str_gives_correct_json_representation():
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    _filter = PublicIPAddress.not_in(items)
    expected = NOT_IN.format("publicIpAddress", *items)
    assert str(_filter) == expected


def test_removable_media_name_exists_str_gives_correct_json_representation():
    _filter = RemovableMediaName.exists()
    expected = EXISTS.format("removableMediaName")
    assert str(_filter) == expected


def test_removable_media_name_not_exists_str_gives_correct_json_representation():
    _filter = RemovableMediaName.not_exists()
    expected = NOT_EXISTS.format("removableMediaName")
    assert str(_filter) == expected


def test_removable_media_name_eq_str_gives_correct_json_representation():
    _filter = RemovableMediaName.eq("test_name")
    expected = IS.format("removableMediaName", "test_name")
    assert str(_filter) == expected


def test_removable_media_name_not_eq_str_gives_correct_json_representation():
    _filter = RemovableMediaName.not_eq("test_name")
    expected = IS_NOT.format("removableMediaName", "test_name")
    assert str(_filter) == expected


def test_removable_media_name_is_in_str_gives_correct_json_representation():
    items = ["name1", "name2", "name3"]
    _filter = RemovableMediaName.is_in(items)
    expected = IS_IN.format("removableMediaName", *items)
    assert str(_filter) == expected


def test_removable_media_name_not_in_str_gives_correct_json_representation():
    items = ["name1", "name2", "name3"]
    _filter = RemovableMediaName.not_in(items)
    expected = NOT_IN.format("removableMediaName", *items)
    assert str(_filter) == expected


def test_sha256_exists_str_gives_correct_json_representation():
    _filter = SHA256.exists()
    expected = EXISTS.format("sha256Checksum")
    assert str(_filter) == expected


def test_sha256_not_exists_str_gives_correct_json_representation():
    _filter = SHA256.not_exists()
    expected = NOT_EXISTS.format("sha256Checksum")
    assert str(_filter) == expected


def test_sha256_eq_str_gives_correct_json_representation():
    _filter = SHA256.eq("test_sha256")
    expected = IS.format("sha256Checksum", "test_sha256")
    assert str(_filter) == expected


def test_sha256_not_eq_str_gives_correct_json_representation():
    _filter = SHA256.not_eq("test_sha256")
    expected = IS_NOT.format("sha256Checksum", "test_sha256")
    assert str(_filter) == expected


def test_sha256_is_in_str_gives_correct_json_representation():
    items = ["sha2561", "sha2562", "sha2563"]
    _filter = SHA256.is_in(items)
    expected = IS_IN.format("sha256Checksum", *items)
    assert str(_filter) == expected


def test_sha256_not_in_str_gives_correct_json_representation():
    items = ["sha2561", "sha2562", "sha2563"]
    _filter = SHA256.not_in(items)
    expected = NOT_IN.format("sha256Checksum", *items)
    assert str(_filter) == expected


def test_shared_true_str_gives_correct_json_representation():
    _filter = Shared.true()
    expected = IS.format("shared", "TRUE")
    assert str(_filter) == expected


def test_shared_false_str_gives_correct_json_representation():
    _filter = Shared.false()
    expected = IS.format("shared", "FALSE")
    assert str(_filter) == expected


def test_shared_with_exists_str_gives_correct_json_representation():
    _filter = SharedWith.exists()
    expected = EXISTS.format("sharedWith")
    assert str(_filter) == expected


def test_shared_with_not_exists_str_gives_correct_json_representation():
    _filter = SharedWith.not_exists()
    expected = NOT_EXISTS.format("sharedWith")
    assert str(_filter) == expected


def test_shared_with_eq_str_gives_correct_json_representation():
    _filter = SharedWith.eq("test_user")
    expected = IS.format("sharedWith", "test_user")
    assert str(_filter) == expected


def test_shared_with_not_eq_str_gives_correct_json_representation():
    _filter = SharedWith.not_eq("test_user")
    expected = IS_NOT.format("sharedWith", "test_user")
    assert str(_filter) == expected


def test_shared_with_is_in_str_gives_correct_json_representation():
    items = ["user1", "user2", "user3"]
    _filter = SharedWith.is_in(items)
    expected = IS_IN.format("sharedWith", *items)
    assert str(_filter) == expected


def test_shared_with_not_in_str_gives_correct_json_representation():
    items = ["user1", "user2", "user3"]
    _filter = SharedWith.not_in(items)
    expected = NOT_IN.format("sharedWith", *items)
    assert str(_filter) == expected


def test_shared_with_contains_str_gives_correct_json_representation():
    _filter = SharedWith.contains("test")
    expected = CONTAINS.format("sharedWith", "test")
    assert str(_filter) == expected


def test_shared_with_not_contains_str_gives_correct_json_representation():
    _filter = SharedWith.not_contains("test")
    expected = NOT_CONTAINS.format("sharedWith", "test")
    assert str(_filter) == expected


def test_source_exists_str_gives_correct_json_representation():
    _filter = Source.exists()
    expected = EXISTS.format("source")
    assert str(_filter) == expected


def test_source_not_exists_str_gives_correct_json_representation():
    _filter = Source.not_exists()
    expected = NOT_EXISTS.format("source")
    assert str(_filter) == expected


def test_source_eq_str_gives_correct_json_representation():
    _filter = Source.eq("test_source")
    expected = IS.format("source", "test_source")
    assert str(_filter) == expected


def test_source_not_eq_str_gives_correct_json_representation():
    _filter = Source.not_eq("test_source")
    expected = IS_NOT.format("source", "test_source")
    assert str(_filter) == expected


def test_source_is_in_str_gives_correct_json_representation():
    items = ["source1", "source2", "source3"]
    _filter = Source.is_in(items)
    expected = IS_IN.format("source", *items)
    assert str(_filter) == expected


def test_source_not_in_str_gives_correct_json_representation():
    items = ["source1", "source2", "source3"]
    _filter = Source.not_in(items)
    expected = NOT_IN.format("source", *items)
    assert str(_filter) == expected


def test_tab_url_exists_str_gives_correct_json_representation():
    _filter = TabURL.exists()
    expected = EXISTS.format("tabUrl")
    assert str(_filter) == expected


def test_tab_url_not_exists_str_gives_correct_json_representation():
    _filter = TabURL.not_exists()
    expected = NOT_EXISTS.format("tabUrl")
    assert str(_filter) == expected


def test_tab_url_eq_str_gives_correct_json_representation():
    _filter = TabURL.eq("test_tab_url")
    expected = IS.format("tabUrl", "test_tab_url")
    assert str(_filter) == expected


def test_tab_url_not_eq_str_gives_correct_json_representation():
    _filter = TabURL.not_eq("test_tab_url")
    expected = IS_NOT.format("tabUrl", "test_tab_url")
    assert str(_filter) == expected


def test_tab_url_is_in_str_gives_correct_json_representation():
    items = ["tab1", "tab2", "tab3"]
    _filter = TabURL.is_in(items)
    expected = IS_IN.format("tabUrl", *items)
    assert str(_filter) == expected


def test_tab_url_not_in_str_gives_correct_json_representation():
    items = ["tab1", "tab2", "tab3"]
    _filter = TabURL.not_in(items)
    expected = NOT_IN.format("tabUrl", *items)
    assert str(_filter) == expected
