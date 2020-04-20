# Executing Searches

py42 features a powerful, flexible query system for quickly and easily searching file events and alerts.
This guide explains the syntax for building queries and executing searches.

```eval_rst
.. _anchor_search_file_events:
```
## Search File Events

First, import the required modules and classes and create the SDK:

```python
import py42.sdk
from py42.sdk.queries.fileevents.filters import *
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery

sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

You must create `query_filter.FilterGroup` objects to conduct searches. Filter groups have a type
(in the form of a class), such as `EmailSender`, and an operator (in the form of a function), such as `is_in()`.
Some example filter groups look like this:

```python
email_filter = EmailSender.is_in(["test.user@example.com", "test.sender@example.com"])
exposure_filter = ExposureType.exists()
ip_filter = PrivateIPAddress.eq("127.0.0.1")
```

There are two operators when building `file_event_query.FileEventQuery` objects: `any()` and `all()`.

`any()` gets results where at least one of the filters is true and `all()` gets results where all of the filters are true.

```python
any_query = FileEventQuery.any(email_filter, exposure_filter)
all_query = FileEventQuery.all(exposure_filter, ip_filter)
```

For convenience, the `FileEventQuery` constructor works the same way as `all()`:

```python
all_query = FileEventQuery(exposure_filter, ip_filter)
```

You can put filters in an iterable and unpack them (using the `*` operator) in a `FileEventQuery`. This is a common
use case for programs that need to conditionally build up filters:

```python
# Conditionally appends filters to a list for crafting a query

filter_list = []
if need_shared:
    filter_list.append(Shared.is_true())
elif need_actors:
    actor_filter = Actor.is_in(["foo@example.com", "baz@example.com"])
    filter_list.append(actor_filter)
# Notice the use of the '*' operator to unpack filter_list
query = FileEventQuery(*filter_list)
```

To execute the search, use `securitydata.SecurityModule.search_file_events()`:

```python
# Prints the MD5 hashes of all the files that caused exposure events where files were moved to an external drive.

query = FileEventQuery(ExposureType.eq(ExposureType.REMOVABLE_MEDIA))
response = sdk.securitydata.search_file_events(query)
file_events = response["fileEvents"]
for event in file_events:
    print(event["md5Checksum"])
```

```eval_rst
.. _anchor_search_alerts:
```
## Search Alerts

Alert searches work in a very similar way to file event searches.

To start, import the filters and query object:

```python
from py42.sdk.queries.alerts.filters import *
from py42.sdk.queries.alerts.alert_query import AlertQuery
```

The one difference between constructing alert queries and file event queries is that alert queries require a tenant
ID. You can get the tenant ID from the `sdk.usercontext` object:

```python
# Create a query for getting all open alerts with severity either 'High' or 'Medium'.

filters = [AlertState.eq(AlertState.OPEN), Severity.is_in([Severity.HIGH, Severity.MEDIUM])]
tenant_id = sdk.usercontext.get_current_tenant_id()
# Notice the constructor takes the tenant ID first.
query = AlertQuery(tenant_id, *filters)
```

To execute the search, use the `alerts.AlertClient.search()` method:

```python
# Prints the actor property from each search result
response = sdk.securitydata.alerts.search(query)
alerts = response["alerts"]
for alert in alerts:
    print(alert["actor"])
```
