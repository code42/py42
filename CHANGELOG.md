# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.3 - 2019-05-08

### Added
- `SDK.security.search_file_events()` to search for file events using the Forensic File Search (FFS) service
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
