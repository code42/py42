# File Event Queries - V2

```{eval-rst}
.. autoclass:: py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery
    :members:
    :show-inheritance:
```

## Saved Searches

    # TODO: saved search V2 API is not yet available.


## Filter Classes

The following classes construct filters for file event queries. Each filter class corresponds to a file event detail.
Call the appropriate class method on your desired filter class with the `value` you want to match and it will return a
`FilterGroup` object that can be passed to `FileEventQuery`'s `all()` or `any()` methods to create complex queries
that match multiple filter rules.

Example:

To search for events observed for certain set of documents, you can use the `FileName` and `MD5` filter classes to
construct `FilterGroup`s that will search for matching filenames or (in case someone renamed the sensitive file) the
known MD5 hashes of the files:

    filename_filter = FileName.is_in(['confidential_plans.docx', 'confidential_plan_projections.xlsx'])
    md5_filter = MD5.is_in(['133765f4fff5e3038b9352a4d14e1532', 'ea16f0cbfc76f6eba292871f8a8c794b'])

See [Executing Searches](../userguides/searches.md) for more on building search queries.

### Filter Group Helper Methods

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.v2.file_event_query.create_exists_filter_group
```

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.v2.file_event_query.create_not_exists_filter_group
```

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.v2.file_event_query.create_greater_than_filter_group
```

```{eval-rst}
.. automethod:: py42.sdk.queries.fileevents.v2.file_event_query.create_less_than_filter_group
```

More helper methods for constructing queries can be found in [Shared Query Filters](sharedqueryfilters.md).

### Destination Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.destination_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### Event Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.event_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### File Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.file_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### Process Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.process_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### Risk Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.risk_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### Source Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.source_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### Timestamp Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.timestamp_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

### User Filters

```{eval-rst}
.. automodule:: py42.sdk.queries.fileevents.v2.filters.user_filter
    :members:
    :inherited-members:
    :show-inheritance:
```
