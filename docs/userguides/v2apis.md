## V2 File Events

```{eval-rst}
.. warning:: V1 File Event APIs and query requests are **deprecated**.  They are estimated to be removed late spring 2023. # TODO: PLACEHOLDER (tentative date)
```

For details on the updated File Event Model, see [Code42's support article](https://support.code42.com/) and V2 API documentation on the [Developer Portal](https://developer.code42.com/). # TODO: PLACEHOLDER

## Updating settings

First, update your `use_v2_file_event_data` setting to ensure py42 is using the appropriate V2 APIs:

```python
import py42.sdk
import py42.settings

py42.settings.use_v2_file_event_data = True
```

Leaving this setting as `False` means Py42 will **not** ingest V2 data or use the new corresponding V2 APIs.

## Querying file events

To query for V2 file events, import the corresponding filter modules and `FileEventQuery` object:
```python
import py42.sdk
from py42.sdk.queries.fileevents.v2.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.v2.filters import *
```

alternatively, you can import all the V2 modules at once with:
```python
import py42.sdk
from py42.sdk.queries.fileevents.v2 import *
```

Using the `FileEventQuery` and filter classes, construct a query and search for file events as detailed in the [Executing Searches Guide](searches.md)
