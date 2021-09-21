# Trust Settings

Use py42 to quickly and easily manage trusted activities and resources, including domains and Slack workspaces.

## Create, View or Modify Trusted Activities

To get started create a new trusted activity resource.

```python
from py42.constants import TrustedActivityType

response = sdk.trustedactivities.create(TrustedActivityType.DOMAIN, "test-domain.com")
```
Constants for the trusted activity types are available at [Trusted Activity Type](../methoddocs/constants.html#py42.constants.TrustedActivityType)


Once you've created a trusted activity, or if you're working with an existing one, you can use the trusted activity's `resourceId` to view details about it.

```python
response = sdk.trustedactivities.get(resource_id)

```

You can also access a trusted activity by its `resourceId` to update its details.  For instance, if you wanted to add a description to a trusted activity:

```python
response = sdk.trustedactivities.update(resource_id, description="This is a trusted activity.")
```

To clear the description of a trusted activity, pass an empty string `description=""` to the `update()` method.

```eval_rst
.. important::
    If you try to create with the same value as an already existing activity, you will get a `py42.exceptions.Py42TrustedActivityConflictError`.

```

## View Details for all Trusted Domains

This section describes how to view the details of all trusted activities of the type `DOMAIN`.

```python
from py42.constants import TrustedActivityType

response = sdk.trustedactivities.get_all(type=TrustedActivityType.DOMAIN)

for page in response:
    resources = page["trustResources"]
    for resource in resources:
        print(resource)
```
For complete details, see
 [Trusted Activities](../methoddocs/trustedactivities.md).
