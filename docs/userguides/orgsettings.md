# View or Modify organization settings

Use pycpg to easily view and update the settings for organizations with the `OrgSettings` object.

The `OrgSettings` object is a wrapper around the complex dicts that the CrashPlan `Org` and `OrgSettings` API endpoints expect,
providing helper properties that can be used to get/set values, without having to know the underlying complexity of the APIs.

To get started, create a `OrgSettings` object for a given org_id:

```python
org_settings = sdk.orgs.get_settings(org_id)
```

Some common non-modifiable details about the org are accessible as read-only properties:

```python
>>> org_settings.org_id
424345
>>> org_settings.registration_key
'XXXX-YYYY-AAAA-BBBB'
```

And to change settings, in most cases you can just assign new values to the appropriate attribute:

```python
>>> org_settings.name
'Admin Test Org'
>>> org_settings.name = "Admin Production Org"
```

Configuring device backup defaults for an org is very similar to [configuring backup settings for an individual device](devicesettings.md),
the `OrgSetting` object has a `.device_defaults` property that contains a `DeviceSettingsDefaults` object providing
convenience attributes/methods for configuring defaults for all devices in the org.

```python
>>> org_settings.device_defaults.backup_status_email_enabled
True
>>> org_settings.device_defaults.warning_alert_days
7
>>> org_settings.device_defaults.warning_alert_days = 14
```

Backup set configurations are contained in the `.device_defaults.backup_sets` property, and return a list of `BackupSet`
wrapper classes for each set configured for the org:

```python
>>> org_setting.device_defaults.backup_sets
[<BackupSet: id: 1, name: 'Production Environment - Backup Set'>]
```

See the [Configuring Backup Sets](backupsets.md) guide for details on managing backup set settings.

Once you've made all the desired changes to an `OrgSettings` object, you can post the changes by passing it to the `sdk.orgs.update_settings()` method.

Because there are two endpoints that manage different organization settings values (`/api/Org` and `/api/OrgSettings`), the `sdk.orgs.update_settings()`
method might make up to two requests to the server, depending on what `OrgSetting` values were actually modified. Because of the potential for two
response values, `orgs.update_settings()` returns a `OrgSettingsResponse` namedtuple with the responses from both endpoints (if applicable), along with an
`error` flag that indicates if any errors occurred. If an error occurred, the `org_response` or `org_settings_response` attributes will contain the
`PycpgException` that was raised instead of the `PycpgResponse`.


```python
>>> sdk.orgs.update_settings(org_settings)
OrgSettingsResponse(error=False, org_response=<PycpgResponse [status=200, data={'active': True, 'blocked': False, 'classification': 'BASIC', 'configInheritanceCounts': {}, ...}]>, org_settings_response=None)
```
