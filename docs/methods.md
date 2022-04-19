
# Method Documentation

```{eval-rst}
.. toctree::
    :hidden:
    :maxdepth: 2
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

* [Alerts](methoddocs/alerts.md)
* [Alert Rules](methoddocs/alertrules.md)
* [Archive](methoddocs/archive.md)
* [Audit Logs](methoddocs/auditlogs.md)
* [Backup Sets](methoddocs/backupset.md)
* [Cases](methoddocs/cases.md)
* [Constants](methoddocs/constants.md)
* [Detection Lists](methoddocs/detectionlists.md)
* [Devices](methoddocs/devices.md)
* [Device Settings](methoddocs/devicesettings.md)
* [Exceptions](methoddocs/exceptions.md)
* [File Event Queries](methoddocs/fileeventqueries.md)
* [Legal Hold](methoddocs/legalhold.md)
* [Orgs](methoddocs/orgs.md)
* [Org Settings](methoddocs/orgsettings.md)
* [Response](methoddocs/response.md)
* [Security Data](methoddocs/securitydata.md)
* [Shared Query Filters](methoddocs/sharedqueryfilters.md)
* [Trusted Activities](methoddocs/trustedactivities.md)
* [Users](methoddocs/users.md)
* [User Risk Profiles](methoddocs/userriskprofile.md)
* [Util](methoddocs/util.md)
* [Watchlists](methoddocs/watchlists.md)

```{eval-rst}
.. automodule:: py42.sdk
    :members:
    :show-inheritance:

.. autoclass:: py42.sdk.SDKClient
    :members:
    :show-inheritance:
```
