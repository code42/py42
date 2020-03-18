# Executing Searches

## File Event Searches

First, import the required modules and classes and create the SDK:

    >>> import py42.sdk
    >>> from py42.sdk.queries.fileevents.filters import *
    >>> from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
    >>>
    >>> sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")

You will need to create `query_filter.FilterGroup` objects to conduct searches. Filter Groups have a type,
such as `EmailSender`, and an operator, such as `is_in`. Some example filter groups looks like this:

    >>> email_filter = EmailSender.is_in(["test.user@example.com", "test.sender@example.com"])
    >>> exposure_filter = ExposureType.exists()
    >>> ip_filter = PrivateIPAddress.eq("127.0.0.1")

There are two operators when building `file_event_query.FileEventQuery` objects: `any`, and `all`.
`any` gets results where at least one of the filters is true and `all` gets results where all filters are true.

    >>> any_query = FileEventQuery.any(email_filter, exposure_filter)
    >>> all_query = FileEventQuery.all(exposure_filter, ip_filter)

Filters can be put into an iterable and unpacked into `FileEvetQuery.any()` using the `*` operator. This is a common
use case for programs that need to conditionally build up filters:

    >>> filters = [Source.eq("GMAIL"), Actor.is_in(["foo@example,com", "baz@example.com"])]
    >>> query = FileEventQuery.any(*filters)

To execute the search, use `securitydata.SecurityModule.search_file_events()`:

    >>> response = sdk.securitydata.search_file_events(query)
    >>> file_events = response["fileEvents"]

## Alert Searches

First, import alert filters:

    >>> from py42.sdk.queries.alerts.filters import *
    >>> from py42.sdk.queries.alerts.alert_query import AlertQuery

The syntax for building an alert query is the same as building a file event query. The caveat is
that alert queries require a tenant ID:

    >>> filters = [AlertState.eq("OPEN"), Severity.is_in(["HIGH", "LOW"])]
    >>> tenant_id = sdk.usercontext.get_current_tenant_id()
    >>> query = AlertQuery(tenant_id, *filters)

To execute the search, use `alerts.AlertClient.search()`:

    >>> sdk.securitydata.alerts.search(query)
    >>> alerts = sdk.securitydata.alerts.search(*filters)
