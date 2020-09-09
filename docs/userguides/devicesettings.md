# View or Modify device settings

Use py42 to easily view and update the settings for devices with the `DeviceSettings` object.

The `DeviceSettings` object is a wrapper around the complex nested dict that the Code42 `Computer` API endpoint expects,
providing helper properties that can be used to get/set values, without having to know the underlying nested structure.

To get started, create a `DeviceSettings` object for a given device guid:

```python
device_settings = sdk.devices.get_settings(908765043021)
```

Some common non-modifiable details about the device are accessible as read-only properties:

```python
>>> device_settings.computer_id
12345
>>> device_settings.guid
908765043021
>>> device_settings.org_id
42
>>> device_settings.user_id
494842
>>> device_settings.version
1525200006800
>>> device_settings.available_destinations
{'632540230984925185': 'PROe Cloud, US - West', '43': 'PROe Cloud, US'}
```

And to change settings, in most cases you can just assign new values to the corresponding attribute:

```python
>>> device_settings.name
"Admin's Computer"
>>> device_settings.name = "Bob's Laptop"
```

Because device backup settings are tied to a given "Backup Set", of which there could be more than one, the `DeviceSettings.backup_sets`
property returns a list of `BackupSet` wrapper classes that help manage backup configuration settings.

```python
>>> device_settings.backup_sets
[<BackupSet: id: 1, name: 'Primary - Backup Set'>, <BackupSet: id: 298010138, name: 'Secondary (large files) - Backup Set'>]
```

See the [Configuring Backup Sets](backupsets.md) guide for details on managing backup set settings.


For convenience and logging purposes, all changes are tracked in the `.changes` property of the `DeviceSettings` objects.

```python
>>> device_settings.changes
{'destinations': "{'43': 'PROe Cloud, US <LOCKED>'} -> {'43': 'PROe Cloud, US <LOCKED>', '632540230984925185': 'PROe Cloud, US - West'}"}
```

Once you've made all the desired changes to a `DeviceSettings` object, you can post the changes by passing it to the `sdk.devices.update_settings` method, which returns a `Py42Response` object
with the server response:

```python
>>> sdk.devices.update_settings(device_settings)
<Py42Response [status=200, data={'active': True, 'address': '192.168.74.144:4247', 'alertState': 0, 'alertStates': ['OK'], ...}]>
```
