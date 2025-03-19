
# Method Documentation

```{eval-rst}
.. toctree::
    :hidden:
    :maxdepth: 4
    :glob:

    methoddocs/*
```

The main SDK object by which all other methods are accessed is created by
calling `pycpg.sdk.from_local_account` or `pycpg.sdk.from_jwt_provider`. For example:

```python
import pycpg.sdk

sdk = pycpg.sdk.from_local_account("console.us1.crashPlan.com", "john.doe@example.com", "my_pw")
# access properties on 'sdk' to explore all the available methods
```

```{eval-rst}
.. important::
    `pycpg` only supports token-based authentication.
```

Explore the complete public documentation for `pycpg` below.

* [Archive](methoddocs/archive.md)
* [Audit Logs](methoddocs/auditlogs.md)
* [Backup Sets](methoddocs/backupset.md)
* [Constants](methoddocs/constants.md)
* [Devices](methoddocs/devices.md)
* [Device Settings](methoddocs/devicesettings.md)
* [Exceptions](methoddocs/exceptions.md)
* [Legal Hold](methoddocs/legalhold.md)
* [Legal Hold - API Clients](methoddocs/legalholdapiclient.md)
* [Orgs](methoddocs/orgs.md)
* [Org Settings](methoddocs/orgsettings.md)
* [Users](methoddocs/users.md)
* [Util](methoddocs/util.md)

```{eval-rst}
.. automodule:: pycpg.sdk
    :members:
    :show-inheritance:

.. autoclass:: pycpg.sdk.SDKClient
    :members:
    :show-inheritance:
```
