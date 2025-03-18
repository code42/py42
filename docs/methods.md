
# Method Documentation

```{eval-rst}
.. toctree::
    :hidden:
    :maxdepth: 4
    :glob:

    methoddocs/*
```

The main SDK object by which all other methods are accessed is created by
calling `py42.sdk.from_local_account` or `py42.sdk.from_jwt_provider`. For example:

```python
import py42.sdk

sdk = py42.sdk.from_local_account("console.us.code42.com", "john.doe@example.com", "my_pw")
# access properties on 'sdk' to explore all the available methods
```

```{eval-rst}
.. important::
    `py42` only supports token-based authentication.
```

Explore the complete public documentation for `py42` below.

* [Archive](methoddocs/archive.md)
* [Backup Sets](methoddocs/backupset.md)
* [Constants](methoddocs/constants.md)
* [Devices](methoddocs/devices.md)
* [Device Settings](methoddocs/devicesettings.md)
* [Exceptions](methoddocs/exceptions.md)
* [Legal Hold](methoddocs/legalhold.md)
* [Legal Hold - API Clients](methoddocs/legalholdapiclient.md)
* [Orgs](methoddocs/orgs.md)
* [Org Settings](methoddocs/orgsettings.md)
* [Response](methoddocs/response.md)
* [Users](methoddocs/users.md)
* [Util](methoddocs/util.md)
* [(DEPRECATED) Alerts](methoddocs/alerts.md)
* [(DEPRECATED) Alert Rules](methoddocs/alertrules.md)
* [(DEPRECATED) Audit Logs](methoddocs/auditlogs.md)
* [(DEPRECATED) File Event Queries - V1](methoddocs/fileeventqueries.md)
* [(DEPRECATED) File Event Queries - V2](methoddocs/fileeventqueriesv2.md)
* [(DEPRECATED) Security Data](methoddocs/securitydata.md)
* [(DEPRECATED) Shared Query Filters](methoddocs/sharedqueryfilters.md)
* [(DEPRECATED) Trusted Activities](methoddocs/trustedactivities.md)
* [(DEPRECATED) User Risk Profiles](methoddocs/userriskprofile.md)
* [(DEPRECATED) Watchlists](methoddocs/watchlists.md)

```{eval-rst}
.. automodule:: py42.sdk
    :members:
    :show-inheritance:

.. autoclass:: py42.sdk.SDKClient
    :members:
    :show-inheritance:
```
