# File Event Queries

```eval_rst
.. autoclass:: py42.clients.file_event.FileEventClient
    :members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.file_event_query.FileEventQuery
    :members:
    :show-inheritance:
```

# Filter Classes

Each of the following classes can be used to filter Forensic Search results based on the class's corresponding event
attribute. Call the appropriate classmethod on your desired filter class with the `value` you want to match, and it
will return a FilterGroup object that can be passed to `FileEventQuery`'s `all()` or `any()` methods to combine complex
queries that match multiple filter rules.

Example:

To search for events concerning a certain set of documents, you can use the `FileName` and `MD5` filter classes to
construct FilterGroups that will search for matching filenames or (in case someone renamed the sensitive file) the
known MD5 hashes of the files:

    filename_filter = FileName.is_in(['confidential_plans.docx', 'confidential_plan_projections.xlsx'])
    md5_filter = MD5.is_in(['133765f4fff5e3038b9352a4d14e1532', 'ea16f0cbfc76f6eba292871f8a8c794b'])

## Event Filters

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.EventTimestamp
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.EventType
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.InsertionTimestamp
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.event_filter.Source
    :members:
    :inherited-members:
    :show-inheritance:
```

## File Filters

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileCategory
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileName
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileOwner
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FilePath
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.FileSize
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.MD5
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.file_filter.SHA256
    :members:
    :inherited-members:
    :show-inheritance:
```

## Device Filters

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.DeviceUsername
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.OSHostname
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.PrivateIPAddress
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.device_filter.PublicIPAddress
    :members:
    :inherited-members:
    :show-inheritance:
```

## Cloud Filters

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.Actor
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.DirectoryID
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.Shared
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.SharedWith
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.cloud_filter.SharingTypeAdded
    :members:
    :inherited-members:
    :show-inheritance:
```

## Exposure Filters

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.ExposureType
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.ProcessName
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.ProcessOwner
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaName
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaVendor
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaMediaName
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaVolumeName
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaPartitionID
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.RemovableMediaSerialNumber
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.SyncDestination
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.TabURL
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.exposure_filter.WindowTitle
    :members:
    :inherited-members:
    :show-inheritance:
```

## Email Filters

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailPolicyName
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailSubject
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailRecipients
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailSender
    :members:
    :inherited-members:
    :show-inheritance:
```

```eval_rst
.. autoclass:: py42.sdk.queries.fileevents.filters.email_filter.EmailFrom
    :members:
    :inherited-members:
    :show-inheritance:
```
