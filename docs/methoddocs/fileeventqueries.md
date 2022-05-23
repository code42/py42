# File Event Queries - V1 (DEPRECATED)

```{eval-rst}
.. warning:: V1 file events, saved searches, and queries are **deprecated**.
```
For details on using the new file event data model, see the [V2 File Events User Guide](../userguides/v2apis.md).

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.file_event_query.FileEventQuery
    :members:
    :show-inheritance:
```

## Saved Searches

```{eval-rst}
.. autoclass:: py42.services.savedsearch.SavedSearchService
    :members:
    :show-inheritance:
```

## Filter Classes

The following classes construct filters for file event queries. Each filter class corresponds to a file event detail.
Call the appropriate classmethod on your desired filter class with the `value` you want to match and it will return a
`FilterGroup` object that can be passed to `FileEventQuery`'s `all()` or `any()` methods to create complex queries
that match multiple filter rules.

Example:

To search for events observed for certain set of documents, you can use the `FileName` and `MD5` filter classes to
construct `FilterGroup`s that will search for matching filenames or (in case someone renamed the sensitive file) the
known MD5 hashes of the files:

    filename_filter = FileName.is_in(['confidential_plans.docx', 'confidential_plan_projections.xlsx'])
    md5_filter = MD5.is_in(['133765f4fff5e3038b9352a4d14e1532', 'ea16f0cbfc76f6eba292871f8a8c794b'])

See [Executing Searches](../userguides/searches.md) for more on building search queries.

### Event Filters

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.util.create_exists_filter_group
```

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.util.create_not_exists_filter_group
```

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.util.create_greater_than_filter_group
```

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.util.create_less_than_filter_group
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.EventTimestamp
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.EventType
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.InsertionTimestamp
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.Source
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.MimeTypeMismatch
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.OutsideActiveHours
    :members:
    :inherited-members:
    :show-inheritance:
```

### File Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileCategory
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileName
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileOwner
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FilePath
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileSize
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.MD5
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.SHA256
    :members:
    :inherited-members:
    :show-inheritance:
```

### Device Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.DeviceUsername
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.OSHostname
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.PrivateIPAddress
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.PublicIPAddress
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.DeviceSignedInUserName
    :members:
    :inherited-members:
    :show-inheritance:
```

### Cloud Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.Actor
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.DirectoryID
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.Shared
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.SharedWith
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.SharingTypeAdded
    :members:
    :inherited-members:
    :show-inheritance:
```

### Exposure Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.ExposureType
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.ProcessName
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.ProcessOwner
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaName
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaVendor
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaMediaName
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaVolumeName
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaPartitionID
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaSerialNumber
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.SyncDestination
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.SyncDestinationUsername
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.TabURL
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.WindowTitle
    :members:
    :inherited-members:
    :show-inheritance:
```

### Email Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailPolicyName
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailSubject
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailRecipients
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailSender
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailFrom
    :members:
    :inherited-members:
    :show-inheritance:
```

### Activity Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.activity_filter.TrustedActivity
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.activity_filter.RemoteActivity
    :members:
    :inherited-members:
    :show-inheritance:
```

### Printer Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.print_filter.Printer
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.print_filter.PrintJobName
    :members:
    :inherited-members:
    :show-inheritance:
```

### Risk Filters

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.risk_filter.RiskIndicator
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.risk_filter.RiskSeverity
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.filters.risk_filter.RiskScore
    :members:
    :inherited-members:
    :show-inheritance:
```
