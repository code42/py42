# Executing Searches

## File Event Searches

First thing is first, import the requires modules and classes and create the SDK:

    >>> import py42.sdk
    >>> from py42.sdk.queries.fileevents.filters import *
    >>> from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
    >>>
    >>> sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")

You will need to use `~file_event_query.FileEventQuery` with groups of
`~query_filter.FilterGroup` as positional arguments. These objects together build up the
necessary JSON to make executing searchers simpler:

    >>> filters = [Source.eq("GMAIL"), Actor.is_in(["foo@example,com", "baz@example.com"])]
    >>> query = FileEventQuery.any(*filters)

To execute the search, use `~securitydata.SecurityModule.search_file_events`
with a list of filters as positional arguments:

    >>> response = sdk.securitydata.search_file_events(query)
    >>> file_events = response["fileEvents"]

Alert Searches
--------------

    >>> from py42.sdk.queries.alerts.filters import *
    >>> from py42.sdk.queries.alerts.alert_query import AlertQuery

The syntax for alert searches is the same as file event searches. The caveat is
that a tenant ID is required when creating the `~alert_query.AlertQuery`:

    >>> filters = [AlertState.eq("OPEN"), Severity.is_in(["HIGH", "LOW"])]
    >>> tenant_id = sdk.usercontext.get_current_tenant_id()
    >>> query = AlertQuery(tenant_id, *filters)

To execute the search, use `~alerts.AlertClient.search`:

    >>> sdk.securitydata.alerts.search(query)
