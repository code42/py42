# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The intended audience of this file is for py42 consumers -- as such, changes that don't affect
how a consumer would use the library (e.g. adding unit tests, updating documentation, etc) are not captured here.

## 1.15.1 - 2021-06-22

### Changed

- The `DateObserved` alert query filter now parses timestamps using microsecond precision.
- Change JWT auth token label from `v3_user_token` to `Bearer` when authenticating against the `/c42api/v3/auth/jwt` endpoint.

### Fixed

- Python2.7 bug where non-unicode `str` timestamps would fail when used in a query filter.

## 1.15.0 - 2021-06-16

### Fixed

- Issue where `sdk.detectionlists.create_user()` would always fail because of API changes.
    The method has been deprecated and now returns the response from `sdk.detectionlists.get()`.

### Added

- New custom exception `Py42UnableToCreateProfileError` that is raised when calling the
    method `sdk.detectionlists.create_user()` due to the user not existing in Code42 or
    is already in the process of being created on the back-end.

- `SyncDestinationUsername` filter class to `py42.sdk.queries.fileevents.filters.exposure_filter` module.

## 1.14.2 - 2021-05-07

### Fixed

- Issue where `sdk.users.get_roles()` was using a deprecated API.

## 1.14.1 - 2021-04-29

### Fixed

- Issue when calling `sdk.alerts.update_state()` without specifying a `note` parameter
    would set the existing alert's note's message to the empty string.

### Added

- Custom exception `Py42OrgNotFoundError`.

### Changed

- `sdk.users.get_all()` now raises `Py42OrgNotFoundError` when the given `org_uid`
    was not found.

- `sdk.users.get_page()` now raises `Py42OrgNotFoundError` when the given `org_uid`
    was not found.

## 1.14.0 - 2021-04-20

### Added

- New method `sdk.alerts.search_all_pages()` to retrieve all alert pages.

- New method `sdk.alerts.get_aggregate_data()` to get alert summary and observations.

### Changed

- Method `sdk.alerts.search()` now accepts optional arguments `page_num` and `page_size`.

- Methods `sdk.cases.update()` and `sdk.cases.create()` now raise custom exception
    `Py42InvalidCaseUserError` when trying to add an invalid user as a subject or an
  assignee of a case.

- `sdk.cases.update()` now raises `Py42CaseNameExistsError` when the name of the case
  already exists in the system.

## 1.13.0 - 2021-04-14

### Added

- `sdk.legalhold.get_events_page()` to get a page of legal hold events.

- `sdk.legalhold.get_all_events()` to search for legal hold events.

- `sdk.users.update_user()` to update an existing user in Code42.

- `sdk.alerts.update_note()` to add or update a note regarding an alert.

- `sdk.from_jwt_provider()` method to create an `SDKClient` that supports custom auth mechanism.

### Fixed

- Bug where proxy settings were not being applied correctly.

- Bug where 500 errors would not raise during `sdk.users.create_user()`.

## 1.11.1 - 2021-02-02

### Changed

- `sdk.cases.create()` now raises `Py42CaseNameExistsError` when the case name already
  exists in the system.

- `sdk.cases.create()` now raises `Py42DescriptionLimitExceededError` when the description
  is more than 250 characters.

- `sdk.cases.update()` now raises `Py42DescriptionLimitExceededError` when the description
  is more than 250 characters.

- `sdk.cases.file_events.add()` now raises `Py42CaseAlreadyHasEventError` when the same
  event is added to a case more than once.

- `sdk.cases.file_events.add()` now raises `Py42UpdateClosedCaseError` when the event is
  added to a closed case.

- `sdk.cases.file_events.delete()` now raises `Py42UpdateClosedCaseError` when the event
  is deleted from a closed case.

## 1.11.0 - 2021-01-20

### Changed

- `sdk.legalhold.get_custodians_page()` now raises `Py42LegalHoldCriteriaMissingError` when missing one of the required options.

### Added

- Python 3.9 support.

- `sdk.cases` methods:
    - `sdk.cases.create()`
    - `sdk.cases.get_all()`
    - `sdk.cases.get_page()`
    - `sdk.cases.export_summary()`
    - `sdk.cases.get()`
    - `sdk.case.update()`

- `sdk.cases.file_events` methods for managing file events associated with a given case:
    - `sdk.cases.file_events.add()`
    - `sdk.cases.file_events.delete()`
    - `sdk.cases.file_events.get()`
    - `sdk.cases.file_events.get_all()`

## 1.10.1 - 2020-12-16

### Fixed

- Bug where trying to retrieve device settings for a device on legal holds caused an exception to be raised.

## 1.10.0 - 2020-12-14

### Fixed

- Bug that occurs when trying to add a user to an alert rule who had never been on any detection list before.

- Bug where an empty destination list in a device's backup set broke creation of DeviceSettings objects for that device.

- Bug where all 401 Unauthorized error responses were being raised as Py42MFARequired exceptions.

- Bug where requests to storage nodes were only using single-use tokens for authentication, causing many extraneous requests.

### Added

- `sdk.archive.stream_to_device()` for pushing a restore to another device.

- Added new exception `Py42CloudAliasLimitExceededError` to throw if `add_cloud_alias()` throws `400` and body contains
reason `Cloud usernames must be less than or equal to`.

- Added new exception `Py42UserNotOnListError` to throw error if `remove()` throws `404` when the user is not on a detection list.

- Added new exception `Py42TooManyRequestsError` to raise errors with 429 HTTP status code.

- Added new method `sdk.securitydata.search_all_file_events()` to retrieve all events when events are more than 10,000.

- Added new custom exception `sdk.exceptions.Py42InvalidPageToken` that gets raised when the page token from
  `sdk.securitydata.search_all_file_events()` causes a specific bad request error.

## 1.9.0 - 2020-10-02

### Changed

- The following methods now support string timestamp formats (`yyyy-MM-dd HH:MM:SS`) as well as a `datetime` instance:
    - `sdk.auditlogs.get_page()`, arguments `begin_time` and `end_time`.
    - `sdk.auditlogs.get_all()`, arguments `begin_time` and `end_time`.
    - `sdk.securitydata.get_all_plan_security_events()`, arguments `min_timestamp` and `max_timestamp`.
    - `sdk.securitydata.get_all_user_security_events()`, arguments `min_timestamp` and `max_timestamp`.

- The `departure_date` parameter for methods:
    - `sdk.detectionlists.departing_employee.add()`
    - `sdk.detectionlists.departing_employee.update_departure_date()`
    now support a `datetime` instance.

- The following methods on timestamp-based query filters (e.g. `EventTimestamp`, `DateObserved`) now support string timestamp format (`yyyy-MM-dd HH:MM:SS`) as well as a `datetime` instance:
    - `on_or_before()`
    - `or_or_after()`
    - `in_range()`

### Removed

- Removed faulty `within_the_last()` method from `sdk.queries.alerts.filters.alert_filter.DateObserved`.

### Added
- Added new exception `Py42UserAlreadyExistsError` to throw if `create_user()` throws `500` and body contains
`USER_DUPLICATE`

- Added `Py42ActiveLegalHoldError` exception when attempting to deactivate a user or device in an active legal hold.
    - `py42.sdk.users.deactivate()`
    - `py42.sdk.devices.deactivate()`

- Added additional user-adjustable setting for security events page size:
    - `py42.settings.security_events_per_page`

- Page page_number and page_size parameters for saved search queries:
    - `py42.securitydata.savedsearches.get_query()`
    - `py42.securitydata.savedsearches.execute()`

- `sdk.alerts.update_state()` method to update state.

- Support for two-factor authentication in `sdk.from_local_account()`

- `OrgSettings` and `DeviceSettings` classes to help with Org and Device setting management.
    - `sdk.orgs.get_settings(org_id)` now returns an instance of `OrgSettings` which can be used to view
        existing Org settings and modify them by passing the updated `OrgSettings` object to `sdk.orgs.update_settings()`
    - `sdk.devices.get_settings(org_id)` now returns an instance of `DeviceSettings` which can be used to view
        existing Device settings and modify them by passing the updated `DeviceSettings` object to `sdk.devices.update_settings()`

- `sdk.auditlogs` method:
    - `sdk.auditlogs.get_page()`
    - `sdk.auditlogs.get_all()`

### Changed

- `py42.sdk.queries.query_filter.filter_attributes` renamed to `py42.util.get_attribute_keys_from_class`

## 1.8.2 - 2020-09-30

### Fixed

- Corrected an issue that caused `sdk.detectionlists.departing_employee.get_all()`
  and `sdk.detectionslists.high_risk_employee.get_all()` to only return the first page (first 100) records. This same issue also caused other `get_all_X()` methods to only return the first page if the requested `page_size` was less than `settings.items_per_page`.

### Added

- `page_size` parameter to:
  - `sdk.detectionlists.departing_employee.get_all()`
  - `sdk.detectionlists.high_rsik_employee.get_all()`

## 1.8.1 - 2020-08-28

### Fixed

- Corrected error logic for trying to add or remove users from a system rule.

## 1.8.0 - 2020-08-27

### Removed

- Removed `tenant_id` parameter from methods:
    - `sdk.alerts.get_details()`
    - `sdk.alerts.resolve()`
    - `sdk.alerts.reopen()`

## Fixed

- Issue that in rare circumstance could cause py42 to exhaust network sockets. This could sometimes occur if you were running a multi-threaded program that communicated with many Code42 storage nodes.

### Added

- Methods for obtaining archive information:
    - `sdk.archive.get_by_archive_guid`
    - `sdk.archive.get_all_by_device_guid`

- Debug logs for restore progress during the method call `py42.archive.stream_from_backup()`.
- [.netrc](https://ec.haxx.se/usingcurl/usingcurl-netrc) support. Calling `py42.sdk.from_local_account()` with no username and password will now result in py42 attempting to authenticate via an entry in your `.netrc` file, if you have one.

- `py42.constants.SortDirection` constants `DESC` and `ASC`.

- `sdk.detectionlists.departing_employee.DepartingEmployeeFilters` constants `OPEN`,
    `EXFILTRATION_30_DAYS`, `EXFILTRATION_24_HOURS`, and `LEAVING_TODAY`.

- `sdk.detectionlists.high_risk_employee.HighRiskEmployeeFilters` constants `OPEN`,
    `EXFILTRATION_30_DAYS`, and `EXFILTRATION_24_HOURS`.

- Methods for calling the agent-state APIs:
    - `sdk.devices.get_agent_state()`
    - `sdk.devices.get_agent_full_disk_access_state()`
    - `sdk.orgs.get_agent_state()`
    - `sdk.orgs.get_agent_full_disk_access_states()`

- Exception classes (`py42.exceptions`)
    - `Py42ResponseError`
    - `Py42UserAlreadyAddedError`
    - `Py42LegalHoldNotFoundOrPermissionDeniedError`
    - `Py42InvalidRuleOperationError`

- Methods for getting individual response pages:
    - `sdk.detectionlists.departing_employee.get_page()`
    - `sdk.detectionlists.high_risk.get_page()`
    - `sdk.users.get_page()`
    - `sdk.devices.get_page()`
    - `sdk.orgs.get_page()`
    - `sdk.legalhold.get_matters_page()`
    - `sdk.legalhold.get_custodians_page()`
    - `sdk.alerts.get_rules_page()`

- Added enum object `py42.modules.detectionlists.RiskTags` with constants:
    - `FLIGHT_RISK`
    - `HIGH_IMPACT_EMPLOYEE`
    - `ELEVATED_ACCESS_PRIVILEGES`
    - `PERFORMANCE_CONCERNS`
    - `SUSPICIOUS_SYSTEM_ACTIVITY`
    - `POOR_SECURITY_PRACTICES`
    - `CONTRACT_EMPLOYEE`

- Added below event filter support
    - TrustedActivity
    - RemoteActivity
    - PrintJobName
    - Printer
    - DeviceSignedInUserName

- Added attributes to below event filters and added `choices` method to return list of all available attributes
    - FileCategory
    - SyncDestination
    - ExposureType
    - Source
    - EventTimestamp
    - EventType
    - SharingTypeAdded
    - RuleSource
    - RuleType
    - AlertState
    - Severity

### Changed

- `sdk.archive.stream_from_backup()` now calculates file sizes and accepts a `file_size_calc_timeout` parameter.
- Parameter `file_path` on `sdk.archive.stream_from_backup()` renamed to `file_paths` and can now take a list of file paths to restore.
- `sdk.detectionlists.departing_employee.add()` now raises `Py42UserAlreadyAddedError` when the user is already on the list.
- `sdk.detectionlists.high_risk_employee.add()` now raises `Py42UserAlreadyAddedError` when the user already on the list.
- `sdk.legalhold.add_to_matter()` now raises `Py42UserAlreadyAddedError` when the user is already on the matter.
- `sdk.legalhold.get_matter_by_uid()` now raises `Py42LegalHoldNotFoundOrPermissionDeniedError` when the user does not have
    access or the ID does not exist.
- `sdk.alerts.rules.add_user()` now raises `Py42InvalidRuleOperationError` on 404s.
- `sdk.alerts.rules.remove_user()` now raises `Py42InvalidRuleOperationError` on 404s.
- `sdk.alerts.rules.remove_all_users()` now raises `Py42InvalidRuleOperationError` on 404s.
- `Py42ArchiveFileNotFoundError` now includes the response.
- `Py42ChecksumNotFoundError` now includes the response.
- `Py42FeatureUnavailableError` now includes the response.
- `Py42StorageSessionInitializationError` now includes the response.

## 1.7.1 - 2020-07-27

### Changed

- `sdk.securitydata.stream_file_by_md5()` now raises `Py42ChecksumNotFoundError` when no matching md5 is found (previously was `Py42ArchiveFileNotFoundError`).
- `sdk.securitydata.stream_file_by_sha256()` now raises `Py42ChecksumNotFoundError` when no matching md5 is found (previously was `Py42Error`).

### Fixed

- functions now return `Py42Response` objects as expected:
    - `sdk.detectionlists.update_user_notes()`
    - `sdk.detectionlists.add_user_risk_tags()`
    - `sdk.detectionlists.remove_user_risk_tags()`
    - `sdk.detectionlists.add_user_cloud_alias()`
    - `sdk.detectionlists.remove_user_cloud_alias()`
- `sdk.archive.get_all_org_cold_storage_archives()` now actually uses parameters `include_child_orgs`, `sort_key` and `sort_dir`.

## 1.7.0 - 2020-07-21

### Added

- Functions for managing role assignment:
    - `sdk.users.get_available_roles()`
    - `sdk.users.get_roles()`
    - `sdk.users.add_role()`
    - `sdk.users.remove_role()`

- `__eq__` and `__hash__` methods to the `py42.sdk.queries.query_filter.QueryFilter` class to enable easier comparison of filters
- `__eq__` and `__contains__` methods to the `py42.sdk.queries.query_filter.FilterGroup` class to enable easier comparison of and membership tests of filter groups

### Changed

- When calling `__str__` or `__iter__` on a `FilterGroup` instance, the filter results have `set()` called on them to remove duplicate filters (if they exist) as well
    as sorts the results. This enables comparing two `FilterGroup`s that might have been constructed differently but ultimately return the exact same results in a query.
- `FilterGroup.filter_clause` property now has a setter, making it easy to change the clause on an existing filter group.

### Removed

- `filter_clause` arg on `FilterGroup.from_dict` method. The clause will automatically be derived from the dict itself.

## 1.6.2 - 2020-07-10

### Added

- `data` to `Py42Response`. This allows a developer to retrieve the full dict of the response under the `data` json node, if present, enabling the use of typical dict functions such as `get()`.

- `content` to `Py42Response`. This exposes the underlying `requests.Response.content`, which contains the fully body of the response as a byte array.

## 1.6.1 - 2020-07-09

### Fixed

- An issue where `sdk.securitydata.stream_file_by_md5()` and `sdk.securitydata.stream_file_by_sha256()` would return streams containing an error message instead of properly failing.

- An issue where streaming methods would load the stream completely into memory instead of retrieving it one chunk at a time.

## 1.6.0 - 2020-06-30

### Added

- Make `ExposureType.OUTSIDE_TRUSTED_DOMAINS` constant available.
- `sdk.securitydata` methods
    - `stream_file_by_sha256()`
    - `stream_file_by_md5()`

### Changed

- `email` is now a required param on `py42.users.create_user()`.

### Removed

- Faulty `py42.orgs.get_by_name()` method. Use `py42.orgs.get_all()` and/or any of the other `get_by_()` methods.

## 1.5.1 - 2020-06-17

### Fixed

- An unintended regression that caused `import py42.sdk.settings.debug` to fail.

### Changed

- For security reasons, debug output no longer logs the headers on http requests.

## 1.5.0 - 2020-06-16

### Added

- Ability for users to provide their own logger for debug logging
- adds `sdk.detectionlists.refresh_user_scim_attributes()` to update user SCIM attributes in detection lists.

### Fixed

- An issue that caused requests to `sdk.alerts.rules.get_all()`, `sdk.alerts.rules.get_all_by_name()`, and `sdk.alerts.rules.get_by_observer_id()` to fail due to a change made to their backing api.

### Changed

- The default value of `py42.settings.items_per_page` has been changed to 500 (was 1000).
- Default debug logging moved from print statements to a logger writing to `sys.stderr`
- Debug logging levels now use standard levels from the `logging` module (old levels still work but are now
    automatically mapped to appropriate `logging` module level, with both `debug.DEBUG` and `debug.TRACE` being mapped
    to `logging.DEBUG`, as `DEBUG` is the lowest level of the `logging` module options).

## 1.4.0 - 2020-06-10

### Added

- `get_all_org_cold_storage_archives()` function to `ArchiveModule`, available at `sdk.archive.get_all_org_cold_storage_archives()`.

### Fixed

- `AlertQuery` now defaults to a `page_size` of 500. A change made to the backing api of `sdk.alerts.search()` was causing all requests made with the previous default (10000) to fail.


## 1.3.0 - 2020-06-02

### Added

- `SavedSearchClient` available at `sdk.securitydata.savedsearches` with the following functions:
    - `get()`
    - `get_by_id()`
    - `execute()`

- `get_scim_data_by_uid()` function to `UserClient`, available at `sdk.users.get_scim_data_by_uid()`.

## 1.2.0 - 2020-05-18

### Added

- `sdk.alerts.rules.get_by_observer_id()` to look up an alert rule by its observer id.

### Changed

- The following methods that required either a single str or list of string argument can now also accept a tuple of strings:
    - `sdk.alerts.get_details()`
    - `sdk.alerts.resolve()`
    - `sdk.alerts.reopen()`
    - `sdk.detectionlists.add_risk_tags()`
    - `sdk.detectionlists.remove_risk_tags()`

#### Removed

- `sdk.alerts.rules.get_by_name()`. Use `sdk.alerts.rules.get_all_by_name()` instead. It functions identically except for that it returns a generator of `Py42Response` objects rather than a list.

## 1.1.3 - 2020-05-12

### Changed

- `sdk.alerts.get_details()` now attempts to parse the "observation data" json string from the response data automatically.

## 1.1.2 - 2020-05-11

### Added

- `RuleId`, `RuleSource` and `RuleType` filter classes to `py42.sdk.queries.alerts.filters.alert_filter` module.

- `Py42Response` items now have `__setitem__` support in order facilitate manipulating a response. For example, `response["users"][0]["username"] = "something else` is now possible.

- `Py42Response` items can now be iterated over multiple times.

## 1.1.1 - 2020-05-04

### Fixed

- Issue causing `detectionlists` functions to fail.

## 1.1.0 - 2020-05-01

### Added

-  `sdk.alert.rules` methods:
    - `add_user()`
    - `remove_user()`
    - `remove_all_users()`
    - `get_all()`
    - `get_by_name()`

-  `sdk.alert.rules.exfiltration` methods:
    - `get()`

-  `sdk.alert.rules.cloudshare` methods:
    - `get()`

-  `sdk.alert.rules.filetypemismatch` methods:
    - `get()`

### Removed

- `sdk.securitydata.alerts`. use `sdk.alerts` instead.

## 1.0.1 - 2020-04-29

### Added

- `sdk.archive.update_cold_storage_purge_date()`, allowing the changing of the date at which a cold storage archive will be purged.

### Changed

- Exceptions that inherit from `Py42HTTPError` now return the original `requests.Response` object on the exception's
    `.response` property instead of a string representation of the `HTTPError` that was raised.

- `departure_date` is now an optional parameter for `sdk.detectionlists.departing_employee.add()`.

- `py42.sdk.queries.alerts.alert_query.AlertQuery` no longer requires a `tenant_id` to be added to the query manually,
    the `AlertClient.search()` method now adds the tenant_id automatically from the user_context.

## 1.0.0 - 2020-04-21

### Changed

- `sdk.detectionlists` methods:
  - `add_cloud_aliases()` > `add_cloud_alias()`
  - `remove_cloud_aliases()` > `remove_cloud_alias`.

The above methods no longer support lists for their `alias` parameter.

## 0.9.0 - 2020-04-17

### Added

- `sdk.detectionlists.departing_employee` methods:
    - `set_alerts_enabled()`

###  Changed

- `sdk.detectionlists.departing_employee` methods:
    - `create()` -> `add()`
    - `resolve()` -> `remove()`
    - `update()` -> `update_departure_date()`
    - `get_by_id()` -> `get()`

## 0.8.1 - 2020-04-16

### Changed

- `sdk.detectionlists` method renames:
    - `create()` -> `create_user()`
    - `get()` -> `get_user()`
    - `get_by_id()` -> `get_user_by_id()`
    - `update_notes()` -> `update_user_notes()`
    - `add_risk_tag()` -> `add_user_risk_tags()`
    - `remove_risk_tag()` -> `remove_user_risk_tags()`
    - `add_cloud_alias()` -> `add_user_cloud_aliases()`
    - `remove_cloud_alias()` -> `remove_user_cloud_aliases()`

## 0.8.0 - 2020-04-15

### Added

- `sdk.detectionlists` methods:
  - `update_notes()`
  - `remove_risk_tag()`
  - `add_risk_tag()`
  - `add_cloud_alias()`
  - `remove_cloud_alias()`
  - `create()`
  - `get()`
  - `get_by_id()`

- `sdk.detectionlists.high_risk_employee` methods:
    - `add()`
    - `remove()`
    - `get()`
    - `search()`
    - `set_alerts_enabled()`

## 0.7.0 - 2020-04-10

### Removed

- Parameter `classification` removed from `OrgClient.create_org()`
- Parameter `legal_hold_membership_uid` removed from `LegalHoldClient.get_all_matter_custodians()`
- Removed `ArchiveClient`. Use `ArchiveModule`.
- Removed function `ArchiveModule.get_data_key_token()`.
- Removed function `ArchiveModule.get_web_restore_info()`.
- Parameter `classification` removed from `OrgClient.create_org()`.
- Parameter `legal_hold_membership_uid` removed from `LegalHoldClient.get_all_matter_custodians()`.
- Removed `SecurityClient`. Use `SecurityModule`.
- `py42.sdk.util`. Use `py42.util` instead.
- `py42.sdk.settings`. Use `py42.settings` instead.
- `py42.sdk.response`. Use `py42.response` instead.
- `py42.sdk.usercontext`. Use `py42.usercontext` instead.

## Changed

- Parameter `active_state` was renamed to `active` and now accepts (True, False, or None)
    instead of ("ACTIVE", "INACTIVE", or "ALL") on the following `LegalHoldClient` methods:
    - `get_all_matters()`
    - `get_all_matter_custodians()`
- Parameter `storageaccess` was removed from `SDKClient`. To restore files, just use
    `SDKClient.archive.stream_from_backup()`.
- Parameter `active_state` was renamed to `active` and now accepts (True, False, or None)
    instead of ("ACTIVE", "INACTIVE", or "ALL") on the following `LegalHoldClient` methods:
    - `get_all_matters()`
    - `get_all_matter_custodians()`
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
- `py42.modules.ArchiveModule` methods:
    - `get_all_device_restore_history()` (formerly `get_restore_history_by_device_id()`)
    - `get_all_user_restore_history()` (formerly `get_restore_history_by_user_id()`)
    - `get_all_org_restore_history()` (formerly `get_restore_history_by_org_id()`)
    now all return generator objects that handle paging through restore history.
- Renamed `AlertClient.get_query_details()` to `AlertClient.get_details()`.
- Renamed `SecurityModule.get_plan_security_events()` to `get_all_plan_security_events()`.
- Renamed `SecurityModule.get_user_security_events()` to `get_all_user_security_events()`.

### Added

- py42 specific exceptions at new module `py42.exceptions`:
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
- Parameters `archive_password` and `encryption_key` added to `ArchiveModule.stream_from_backup()`.

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
