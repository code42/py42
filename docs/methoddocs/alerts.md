# Alerts (DEPRECATED)

```{eval-rst}
.. warning:: Incydr functionality is **deprecated**. Use the resources at https://developer.code42.com/ instead.
```

```{eval-rst}
.. autoclass:: py42.clients.alerts.AlertsClient
    :members:
    :show-inheritance:
```

## Filter Classes

The following classes construct filters for alert queries. Each filter class corresponds to an alert detail.
Call the appropriate classmethod on your desired filter class with the `value` you want to match and it will return a
`FilterGroup` object that can be passed to `AlertQuery`'s `all()` or `any()` methods to create complex queries
that match multiple filter rules.

```{eval-rst}
.. automodule:: py42.sdk.queries.alerts.filters.alert_filter
    :members:
    :inherited-members:
    :show-inheritance:
```

```{eval-rst}
.. autoclass:: py42.sdk.queries.alerts.alert_query.AlertQuery
    :members:
    :show-inheritance:
```
