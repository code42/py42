# File Event Queries - V2

For details on using the new file event data model, see the [V2 File Events User Guide](../userguides/v2apis.md).

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery
    :members:
    :show-inheritance:
    :noindex:
```

## Saved Searches

```{eval-rst}
.. important::
    Make sure to set the optional argument `use_v2=True` on saved search functions to get V2 file event data and queries.

```

```{eval-rst}
.. autoclass:: py42.services.savedsearch.SavedSearchService
    :members:
    :show-inheritance:
    :noindex:
```


## Filter Classes

The following classes construct filters for file event queries. Each filter class corresponds to a file event detail.
Call the appropriate class method on your desired filter class with the `value` you want to match and it will return a
`FilterGroup` object that can be passed to `FileEventQuery`'s `all()` or `any()` methods to create complex queries
that match multiple filter rules.

Example:

To search for events observed for certain set of documents, you can use the `file.Name` and `file.MD5` filter classes to
construct `FilterGroup`s that will search for matching filenames or (in case someone renamed the sensitive file) the
known MD5 hashes of the files:

    from py42.sdk.queries.fileevents.v2 import *
    filename_filter = File.Name.is_in(['confidential_plans.docx', 'confidential_plan_projections.xlsx'])
    md5_filter = File.MD5.is_in(['133765f4fff5e3038b9352a4d14e1532', 'ea16f0cbfc76f6eba292871f8a8c794b'])

See [Executing Searches](../userguides/searches.md) for more on building search queries.

### Destination Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.destination
    :members:
    :inherited-members:
    :show-inheritance:
```

### Event Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.event
    :members:
    :inherited-members:
    :show-inheritance:
```

### File Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.file
    :members:
    :inherited-members:
    :show-inheritance:
```

### Process Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.process
    :members:
    :inherited-members:
    :show-inheritance:
```

### Risk Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.risk
    :members:
    :inherited-members:
    :show-inheritance:
```

### Source Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.source
    :members:
    :inherited-members:
    :show-inheritance:
```

### Timestamp Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.timestamp
    :members:
    :inherited-members:
    :show-inheritance:
```

### User Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.user
    :members:
    :inherited-members:
    :show-inheritance:
```
