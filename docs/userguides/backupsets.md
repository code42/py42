# Configuring Backup Sets

CrashPlan devices' backup configurations are managed by "Backup Sets", which can be configured either at the individual
device level, or set as default configurations at the org level.

The pycpg `BackupSet` class can be used to view and change the settings of a given backup set.

`BackupSet` instances are automatically constructed by pycpg and attached to their corresponding `DeviceSettings` or
`OrgSettings` objects, and stored in the `.backup_sets` properties (`DeviceSettings.backup_sets` or
`OrgSettings.device_defaults.backup_sets`).

The following examples will use an individual device's backup set, but all the methods/attributes are the same when
configuring an org device default backup set.

Create a `DeviceSettings` object and get the primary backup set object:

```python
>>> device_settings
>>> device_settings.backup_sets
[<BackupSet: id: 1, name: 'Primary - Backup Set'>, <BackupSet: id: 298010138, name: 'Secondary (large files) - Backup Set'>]
>>> bs = device_settings.backup_sets[0]
```

View/update destinations:

```python
>>> bs.destinations
{'43': 'PROe Cloud, US <LOCKED>'}
>>>
>>> bs.add_destination(587738803578339329)
>>> bs.remove_destination(43)
>>> bs.destinations
{'632540230984925185': 'PROe Cloud, US - West'}
```

View/update backup file selection/exclusion lists:

```python
>>> bs.included_files
['C:/Users/Bob/']
>>> bs.excluded_files
[]
>>>
>>> bs.included_files.append("D:/")
>>> bs.excluded_files.append("C:/Users/Bob/Downloads")
```

You can also replace the existing list with a new one:

```python
>>> bs.included_files = ["C:/Users/", "D:/"]
```

View/update filename exclusion patterns:

```python
>>> bs.filename_exclusions
['.*/Photos/']
>>> bs.filename_exclusions.append(".*/Pictures/")
```
