# Method Documentation

The main SDK object by which all other methods are accessed is created by
calling `py42.sdk.from_local_account`. For example:

```python
import py42.sdk

sdk = py42.sdk.from_local_account("console.us.code42.com", "john.doe@example.com", "my_pw")
# access properties on 'sdk' to explore all the available methods
```

```eval_rst
.. important::
    `py42` cannot be used with SAML or Sigle Sign-On based
    accounts such as Okta or Active Directory. Only accounts that are added by having an administrator create them within the Code42 console are currently supported.
```

Explore the complete public documentation for `py42` below.

* [Orgs](methoddocs/orgs.md)
* [Users](methoddocs/users.md)
* [Devices](methoddocs/devices.md)
* [Security Data](methoddocs/securitydata.md)
* [Legal Hold](methoddocs/legalhold.md)
* [Detection Lists](methoddocs/detectionlists.md)
* [Alerts](methoddocs/alerts.md)
* [Alert Rules](methoddocs/alertrules.md)
* [Shared Query Filters](methoddocs/sharedqueryfilters.md)
* [File Event Queries](methoddocs/filleeventqueries.md)
* [Archive](methoddocs/archive.md)
* [Response](methoddocs/response.md)
* [Exceptions](methoddocs/exceptions.md)
* [Util](methoddocs/util.md)
* [Constants](methoddocs/constants.md)

```eval_rst
.. automodule:: py42.sdk
    :members:
    :show-inheritance:

.. autoclass:: py42.sdk.SDKClient
    :members:
    :show-inheritance:
```
