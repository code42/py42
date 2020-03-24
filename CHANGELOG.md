# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The intended audience of this file is for py42 consumers -- as such, changes that don't affect
how a consumer would use the library (e.g. adding unit tests, updating documentation, etc) are not captured here.

## Unreleased

### Removed

- Parameter `classification` removed from `OrgClient.create_org()`

### Added

- py42 specific exceptions at new module `py42.sdk.exceptions`:
    - `Py42Error`
    - `Py42ArchiveFileNotFoundError`
    - `Py42SessionInitializationError`
    - `Py42FeatureUnavailableError`
    - `Py42SecurityPlanConnectionError`
    - `Py42HTTPError`
    - `Py42BadRequestError`
    - `Py42UnauthorizedError`
    - `Py42ForbiddenError`
    - `Py42NotFoundError`
    - `Py42InternalServerError`

### Changed

- `py42.sdk.archive.stream_from_backup()` now raises `Py42ArchiveFileNotFoundError` when it does not find a file.
- `py42.sdk.alerts` and `py42.sdk.detectionlists` raise `Py42SessionInitializationError` if they are unable to
    connect to the necessary microservice and `Py42FeatureUnavailableError` if their environment does not support
    the microservice.
- `py42.sdk.securitydata.get_security_plan_storage_info_list()` raises `Py42SecurityPlanConnectionError` if it can't
    connect to get plan info.
- Storage node connection issues may raise `Py42StorageSessionInitializationError`.
- All requests may raise a subclass of `Py42HTTPError` denoting which type of HTTP error it is:
    - `Py42BadRequestError`
    - `Py42UnauthorizedError`
    - `Py42ForbiddenError`
    - `Py42NotFoundError`
    - `Py42InternalServerError`

## 0.6.1 - 2020-03-17

### Changed

- To import alert filters, do: `from py42.sdk.queries.alerts.filters import *`
    instead of importing them individually.

## 0.6.0 - 2020-03-16

### Removed

- The following methods from `py42.util`:
    - `get_obj_from_response()`
    - `filter_out_none()`
    - `print_dict()`

- `py42.debug` module. Use `py42.settings.debug` instead.
- `py42.util` module. Use `py42.sdk.util` instead.
- `ArchiveModule.download_from_backup()`. Use `ArchiveModule.stream_from_backup()` instead.

### Changed

All client methods now return a `Py42Response` object that simplifies accessing the most meaningful parts
of the returned JSON object.

Renamed methods to reduce redundancy:

- `SDK` > `SDKClient`
    - `create_using_local_account()` > `from_local_account()`
    - `administration` > `serveradmin`
    - `legal_hold` > `legalhold`
    - `storage` > `storageacess`
    - `security` > `securitydata`
    - `user_context` > `usercontext`
    - `employee_case_management` > `detectionlists`

- `StorageClientFactory`
    - `get_storage_client_from_device_guid()` > `from_device_guid()`
    - `get_storage_client_from_plan_uid()` > `from_plan_info()`

- `StorageClient`
    - `security` > `securitydata`

- `StorageSecurityClient`
    - `get_security_detection_events_for_plan()` > `get_plan_security_events()`
    - `get_security_detection_events_for_user()` > `get_user_security_events()`

- `FileEventClient`
    - `search_file_events()` > `search()`

- `StorageArchiveClient`
    - `search_archive()` > `search()`
    - `get_archive_tree_node()` > `get_file_path_metadata()`
    - `create_web_restore_session()` > `create_restore_session()`
    - `submit_web_restore_job()` > `start_restore()`
    - `get_web_restore_job()` > `get_restore_status()`
    - `cancel_web_restore_job()` > `cancel_restore()`
    - `get_web_restore_job_result()` > `stream_restore_result()`

- `DepartingEmployeeClient`
    - `create_departing_employee()` > `create()`
    - `resolve_departing_employee()` > `resolve()`
    - `get_all_departing_employees()` > `get_all()`
    - `get_case_by_username()` > `get_by_username()`
    - `get_case_by_id()` > `get_by_id()`
    - `update_case()` > `update()`

- `LegalHoldClient`
    - `create_legal_hold()` > `create_matter()`
    - `get_legal_hold_policy_by_uid()` > `get_policy_by_uid()`
    - `get_all_legal_hold_policies()` > `get_all_policies()`
    - `get_legal_hold_by_uid()` > `get_matter_by_uid()`
    - `get_legal_holds()` > `get_all_matters()`
    - `get_legal_hold_memberships()` > `get_all_matter_custodians()`
    - `add_user_to_legal_hold()` > `add_to_matter()`
    - `remove_user_from_legal_hold()` > `remove_from_matter()`
    - `deactivate_legal_hold()` > `deactivate_matter()`
    - `reactivate_legal_hold()` > `reactivate_matter()`
    - `create_legal_hold_policy()` > `create_policy()`
    - `create_legal_hold()` > `create_matter()`

- `AlertClient`
    - `search_alerts()` > `search()`
    - `resolve_alert()` > `resolve()`
    - `reopen_alert()` > `reopen()`

- `OrgClient`
    - `get_orgs()`  > `get_all()`
    - `get_org_by_id()` > `get_by_id()`
    - `get_org_by_uid()` > `get_by_uid()`
    - `block_org()` > `block()`
    - `unblock_org()` > `unblock()`
    - `deactivate_org()` > `deactivate()`
    - `reactivate_org()` > `reactivate()`
    - `get_current_user_org` > `get_current`

- `UserClient`
    - `get_user_by_id()` > `get_by_id()`
    - `get_user_by_uid()` > `get_by_uid()`
    - `get_user_by_username()` > `get_by_username()`
    - `get_current_user()` > `get_current()`
    - `get_users()` > `get_all()`
    - `block_user()` > `block()`
    - `unblock_user()` > `unblock()`
    - `deactivate_user()` > `deactivate()`
    - `reactivate_user()` > `reactivate()`
    - `change_user_org_assignment()` > `change_org_assignment()`

- `DeviceClient`
    - `get_device_by_id()` > `get_by_id()`
    - `get_device_by_guid()` > `get_by_guid()`
    - `get_devices()` > `get_all()`
    - `block_device()` > `block()`
    - `unblock_device()` > `unblock()`
    - `deactivate_device()` > `deactivate()`
    - `reactivate_device()` > `reactivate()`
    - `deauthorize_device()` > `deauthorize()`
    - `get_device_settings()` > `get_settings()`

## 0.5.1 - 2020-02-27

### Fixed

Issue where large API responses were read very slowly.

## 0.5.0 - 2020-02-27

### Added

Support for querying file events by:
- DirectoryID
- EmailRecipients
- EmailSender
- FileCategory
- FileOwner
- ProcessOwner
- ProcessName
- RemovableMediaName
- Shared
- SharedWith
- SharingTypeAdded
- Source
- SyncDestination
- TabURL
- WindowTitle

## 0.4.4 - 2020-02-24

### Changed

- `py42.settings.items_per_page` no long affects `DepartingEmployeeClient.get_all_departing_employees()`, which is now always set at 100 items per page.
- `FileEventQuery` and `AlertQuery` objects will now return up to 10,000 results by default (the previous default value was 100).

### Fixed

- Issue where `DepartingEmployeeClient.get_all_departing_employees()` always resulted in a 400 status code.

## 0.4.3 - 2020-02-21

### Added

- `py42.settings.items_per_page`. This effectively replaces `page_size` for the methods that were changed below.

### Changed

The following resources no longer accept `page_num` and `page_size` parameters and no longer return a
`requests.Response` object:
- `UserClient.get_users()`
- `DeviceClient.get_devices()`
- `OrgClient.get_orgs()`
- `LegalHoldClient.get_legal_holds()`
- `LegalHoldClient.get_legal_hold_memberships()`
- `DepartingEmployeeClient.get_all_departing_employees()`

They instead return a generator object that is iterated over to retrieve all the pages, eliminating the need to
manually compose loops to retrieve each page. For example, the below snippet will retrieve all pages of users:

```python
for page in users.get_users():
    user_list = json.loads(page.text)["data"]["users"]
```

## 0.4.2 - 2020-02-20

### Added

- Support for querying file events by Actor.

## 0.4.1 - 2020-02-20

### Fixed

- Issue where setting `AlertQuery.sort_direction` did not properly apply the specified direction.

## 0.4.0 - 2020-02-19

### Added

- Added `alerts` to `SecurityModule` with
    - `search_alerts()`
    - `get_query_details()`
    - `resolve_alert()`
    - `reopen_alert()`
- For querying alerts, build an `AlertQuery` object with fields:
    - `AlertState`
    - `Description`
    - `Severity`
    - `Actor`
    - `RuleName`
    New filter operators `contains` and `not_contains` for alert string fields.
- Added `EmployeeCaseManagement` module with `departing_employee` with:
    - `create_departing_employee()`
    - `resolve_departing_employee()`
    - `get_all_departing_employees()`
    - `toggle_alerts()`
    - `get_case_by_username()`
    - `get_case_by_id()`
    - `update_case()`
    Access via `py42.SDK.employee_case_management.departing_employee`
- Added `get_current_tenant` to `py42.SDK.administration`.
- Added `py42.SDK.user_context.get_current_tenant_id`.

## 0.3.1 - 2020-02-14

### Added

- `SecurityModule.get_security_plan_storage_info_list()`
- `SecurityModule.get_user_security_events()`
- `SecurityModule.get_plan_security_events()`

### Changed

- Removed `SecurityModule.get_security_event_locations()`. Use `SecurityClient.get_security_event_locations()` instead.
- Removed `get_normalized_security_event_plan_info().` Support for pre-6.7 format security event plan info responses has
been removed, and as a result this method is no longer necessary. Use `SecurityClient.get_security_event_locations()` instead.

### Fixed

- a timeout of 60 seconds is now enforced on all http requests. Previously the timeout was infinite.
This allowed for the possibility of requests that would hang forever under certain circumstances.

## 0.3.0 - 2020-02-03

### Removed

- `py42.sdk.util.queued_logger`. Use loggers in Python's `logging` namespace instead (they are threadsafe).
- `is_async` option from `sdk.create_from_local_account`. This was an intentionally undocumented feature.
- `force_sync`, `then`, and `catch` options from all client requests. These were only meaningful when used with `is_async`.
- `users.for_each_user()`. Loop over `response["data"]["users"]` instead.
- `devices.for_each_device()`. Loop over `response["data"]["computers"]` instead.
- `py42.settings.global_exception_receiver`. Handle your exceptions as you otherwise normally would instead.

## 0.2.2 - 2019-10-15

### Changed

- `ExposureType.any` has been renamed to `ExposureType.exists`

### Fixed

- Issue where `_FileEventFilterTimestampField` disguised localized times as UTC
- Issue where `_FileEventFilterTimestampField` ignored milliseconds
- Issue on Python 3 where `FileEventQuery.__repr__` did not return type `str`

### Added

- `exists` and `not_exists` added to `file_event_query` string fields.
- `InsertionTimestamp` file event filter support

## 0.2.1 - 2019-09-24

### Added

- Python 3.5.0+ support.
- `users.get_user_by_id()`
- `orgs.get_org_by_id()`
- `devices.get_device_by_id()`

### Fixed

- Issue that caused `users.for_each_user()` and `devices.for_each_device()` to only apply filter criteria to the first
 1000 items returned.

## 0.2.0 - 2019-09-13

### Added

- `SecurityModule.get_security_detection_event_client`

### Removed

- The following methods from `SecurityModule`.
Use `StorageSecurityClient` (via `SecurityModule.get_security_detection_event_client`) instead.
    - `get_security_detection_events_for_user()`
    - `get_security_detection_events_summary()`

- `get_security_detection_events` from `StorageSecurityClient`. Use `get_security_detection_events_for_plan()`,
 `get_security_detection_events_for_user()`, or `get_security_detection_event_summary()` instead.

- `include_files` and `event_types` parameters from `StorageSecurityClient.get_security_detection_event_summary()`.
These had no effect.

## 0.1.10 - 2019-09-12

### Added

- Request URL to request exception message

## 0.1.9 - 2019-09-11

### Fixed

- Issue with creating security plan clients when a session for one client failed to be created

## 0.1.8 - 2019-09-11

### Fixed

- Regression that removed an optimization that allowed user to make requests to the same storage node without
 getting a new storage auth token for each request

## 0.1.7 - 2019-09-09

### Fixed

- Bug in authentication handling logic that caused authentication tokens to not automatically renew properly when
 they expired.
- Bug in creating security plan clients that caused some clients to not be created for users with multiple plans or archives

## 0.1.6 – 2019-07-30

### Fixed

- Issues with unicode support in `securitydata.search_file_events()` and `archive.download_from_backup()`

## 0.1.5 - 2019-07-13

### Fixed

- Bug in the path-matching logic of `archive.download_from_backup` that caused:
  - downloads to fail if the drive/root path didn't match, case-sensitive
  - the API to return `None` instead of raising an exception

## 0.1.4 - 2019-05-31

### Added

 - requests made by py42 now use a user agent string that contains the py42 version and python version.
 This user agent string can be retrieved using `py42.settings.get_user_agent_string()`
 - A custom suffix can be added to the end of this user agent string by using `py42.settings.set_user_agent_suffix()`.
 - `SDK.users.get_users()` and `SDK.devices.get_devices()` now both support a `q` parameter that can be used to check
 common distinguishing fields on those items for an input string (e.g. `SDK.users.get_user(q="test")` will return all
  users whose username or email address contain "test").

### Changed

 - `SDK.archive.download_from_backup()` will now download the most recent non-deleted version of a file. Previously,
file paths that were deleted would not be downloaded.

### Fixed

 -  Asynchronously searching for file events and then later attempting to download a file with the same SDK object
 no longer hangs indefinitely.

## 0.1.3 - 2019-05-08

### Added

- `SDK.securitydata.search_file_events()` to search for file events using the Forensic File Search (FFS) service
- `py42.sdk.file_event_query` module with classes to easily build file event queries
- Ability to print various levels of debug statements for troubleshooting purposes. See `settings.debug_level`
- [pytest](https://docs.pytest.org/) test framework

### Changed

- Merged `SDK.restore` with `SDK.archive`
    - `RestoreModule` was renamed to `ArchiveModule`
    - `RestoreClient` merged into `ArchiveClient`
    - `StorageRestoreClient` merged into `StorageArchiveClient`

### Removed

- Tests from distribution package

## 0.1.2 - 2019-04-09

### Added

- `SDK.restore.download_from_backup()`
- `SDK.users.change_user_org_assignment()`

### Changed

- Simplified APIs
    - Merged and flattened modules under `authority` and `storage`.
        - Example: `SDK.authority.admininstration.users` became `SDK.users`
    - You no longer need to know whether you're connecting to an authority or storage node.

## 0.1.1 - 2019-03-12

### Added

- Added to `SDK.authority.administration.orgs` module:
    - `create_org()`
    - `get_org_by_uid()`
    - `block_org()`
    - `unblock_org()`
    - `deactivate_org()`
    - `reactivate_org()`
- Added to `SDK.authority.administration.device` module:
    - `get_device_by_guid()`
    - `block_device()`
    - `unblock_device()`
    - `deauthorize_device()`
    - `for_each_device()`
    - `get_device_settings()`
    - `deactivate_device()`
    - `reactivate_device()`
- Added to `SDK.authority.administration.users` module:
    - `create_user()`
    - `get_user_by_uid()`
    - `get_user_by_username()`
    - `block_user()`
    - `unblock_user()`
    - `deactivate_user()`
    - `reactivate_user()`
- Added `SDK.authority.legal_hold` module with:
    - `create_legal_hold_policy()`
    - `create_legal_hold()`
    - `get_legal_hold_policy_by_uid()`
    - `get_all_legal_hold_policies()`
    - `get_legal_hold_by_uid()`
    - `get_legal_holds()`
    - `get_legal_hold_memberships()`
    - `add_user_to_legal_hold()`
    - `remove_user_from_legal_hold()`
    - `deactivate_legal_hold()`
    - `reactivate_legal_hold()`
- Added `SDK.authority.archive` module with:
    - `get_data_key_token()`
    - `get_backup_sets()`
- Added to `SDK.authority.restore` module:
    - `get_web_restore_info()`
- Added `SDK.storage.archive` module with:
    - `search_archive()`
    - `get_file_size()`
    - `get_archive_tree_node()`
- Added `SDK.storage.restore` module with:
    - `create_web_restore_session()`
    - `submit_web_restore_job()`
    - `get_web_restore_job()`
    - `cancel_web_restore_job()`
    - `get_web_restore_job_result()`
- Added setup.py to support package installation

### Changed

- Renamed `SDK.device.get_computers()` to `SDK.device.get_devices()`
