# V2 File Events

```{eval-rst}
.. warning:: V1 file events, saved searches, and queries are **deprecated**.
```

For details on the updated File Event Model, see the V2 File Events API documentation on the [Developer Portal](https://developer.code42.com/api/#tag/File-Events).

## Querying file events

To query for V2 file events, import the V2 filter modules and `FileEventQuery` class with:
```python
from py42.sdk.queries.fileevents.v2 import *
```

Using the `FileEventQuery` and filter classes, construct a query and search for file events as detailed in the [Executing Searches Guide](searches.md).

## Saved Searches

All saved search methods functions have an additional optional `use_v2=False` argument.  If set to `True`, the saved search module will ingest from the V2 saved search APIs.  The `use_v2` argument defaults to `False` and the V1 saved searches are still available.

For example, use the following to view all saved searches with the new V2 apis:

```python
import py42.sdk

sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
sdk.securitydata.savedsearches.get(use_v2=True)
```

Retrieving saved searches with V2 settings enabled will retrieve existing V1 saved search queries translated to the V2 model.  Existing V1 queries that cannot be properly converted to V2 will be omitted from the response.
