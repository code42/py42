# Executing Searches

py42 features a powerful, flexible query system for quickly and easily searching file events and alerts.
This guide explains the syntax for building queries and executing searches.

```{eval-rst}
.. _anchor_search_file_events:
```
## Search File Events

To query for V2 file events, import the required modules and classes and create the SDK:
```python
import py42.sdk
from py42.sdk.queries.fileevents.v2 import *
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

V1 events are **DEPRECATED**.  If you need to build V1 queries, the corresponding V1 modules can be imported in a similar manner.

```python
from py42.sdk.queries.fileevents.v1 import *
```

**For more details on updating to V2 file events, see the [V2 File Events Guide](v2apis.md)**

You must create `query_filter.FilterGroup` objects to conduct searches. Filter groups have a type
(in the form of a class), such as `email.Sender`, and an operator (in the form of a function), such as `is_in()`.
Some example filter groups look like this:

```python
from py42.sdk.queries.fileevents.v2 import *
source_email_filter = source.EmailSender.is_in(["test.user@example.com", "test.sender@example.com"])
event_action_filter = event.Action.exists()
destination_ip_filter = destination.PrivateIpAddress.eq("127.0.0.1")
```

It is also possible to create `query_filter.FilterGroups` from raw JSON. For example:

```python
raw_json = """{"filterClause":"AND","filters":[{"display":null,"value":"P1D","operator":"WITHIN_THE_LAST","term":"eventTimestamp"}]}"""
json_dict = json.loads(raw_json)
filter_group = FilterGroup.from_dict(json_dict)
```

```{eval-rst}
.. important::
    The filter terms and query objects for file events have changed for V2.  Make sure you're using the appropriate modules to construct your queries.
```

There are two operators when building `file_event_query.FileEventQuery` objects: `any()` and `all()`.

`any()` gets results where at least one of the filters is true and `all()` gets results where all of the filters are true.

```python
any_query = FileEventQuery.any(source_email_filter, event_action_filter)
all_query = FileEventQuery.all(event_action_filter, destination_ip_filter)
```

For convenience, the `FileEventQuery` constructor works the same way as `all()`:

```python
all_query = FileEventQuery(event_action_filter, destination_ip_filter)
```

You can put filters in an iterable and unpack them (using the `*` operator) in a `FileEventQuery`. This is a common
use case for programs that need to conditionally build up filters:

```python
# Conditionally appends filters to a list for crafting a query

filter_list = []
if need_trusted:
    filter_list.append(risk.Trusted.is_true())
elif need_user_emails:
    user_email_filter = user.Email.is_in(["foo@example.com", "baz@example.com"])
    filter_list.append(user_email_filter)
# Notice the use of the '*' operator to unpack filter_list
query = FileEventQuery(*filter_list)
```

To execute the search, use `securitydata.SecurityModule.search_file_events()`:

```python
# Prints the MD5 hashes of all the events where files were read by browser or other app.

query = FileEventQuery(event.Action.eq(event.Action.APPLICATION_READ))
response = sdk.securitydata.search_file_events(query)
file_events = response["fileEvents"]
for event in file_events:
    print(event["file"]["hash"]["md5"])
```

If the number of events exceeds 10,000 against a query, use `securitydata.SecurityModule.search_all_file_events()`:

```python
query = FileEventQuery(event.Action.eq(event.Action.APPLICATION_READ))
response = sdk.securitydata.search_all_file_events(query)
file_events = response["fileEvents"]
for event in file_events:
    print(event["file"]["hash"]["md5"])
while response["nextPgToken"] is not None:
    response = sdk.securitydata.search_all_file_events(query, page_token=response["nextPgToken"])
    file_events = response["fileEvents"]
    for event in file_events:
        print(event["file"]["hash"]["md5"])
```

```{eval-rst}
.. _anchor_search_alerts:
```
## Search Alerts

Alert searches work in a very similar way to file event searches.

To start, import the filters and query object:

```python
from py42.sdk.queries.alerts.filters import *
from py42.sdk.queries.alerts.alert_query import AlertQuery

# Create a query for getting all open alerts with severity either 'High' or 'Medium'.

filters = [AlertState.eq(AlertState.OPEN), Severity.is_in([Severity.HIGH, Severity.MEDIUM])]
query = AlertQuery(*filters)
```

To execute the search, use the `alerts.AlertClient.search()` method:

```python
# Prints the actor property from each search result
response = sdk.alerts.search(query)
alerts = response["alerts"]
for alert in alerts:
    print(alert["actor"])
```
