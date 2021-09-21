# Cases

Use py42 to quickly and easily manage cases.

## Create, View or Modify Cases

To get started create a new case.

```python
case = sdk.cases.create("new-case")
```

Once you've created a case, or if you're working with an existing one, you can use the case's `number` to view details about that case.

```python

# view details about a case
case = sdk.cases.get(case_number)

```

You can also access a case by its `number` to update its details.  For instance, if you wanted to update a case's status to `CLOSED`:

```python
from py42.constants import CaseStatus

response = sdk.cases.update(case_number, status=CaseStatus.CLOSED)
```

Case statuses can be set to either `OPEN` or `CLOSED`.  Constants for these statuses are available at [Case Status](../methoddocs/constants.html#py42.constants.CaseStatus)

## View Details for all OPEN Cases

This section describes how to view the details of all cases with an `OPEN` status.

```python
from py42.constants import CaseStatus

response = sdk.cases.get_all(status=CaseStatus.OPEN)

for page in response:
    cases = page["cases"]
    for case in cases:
        print(case)
```

For complete details, see
 [Cases](../methoddocs/cases.md).
