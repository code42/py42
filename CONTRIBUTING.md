# Contributing to the Code42 Python SDK

## Changes

Document all notable changes in CHANGELOG.md per principles and guidelines at [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## Tests

We use the [pytest](https://docs.pytest.org/) test framework.

To run all tests, run this at the root of the repo:

```bash
python setup.py test
```

### Writing tests

#### Do

Put actual before expected values in assert statements. Pytest assumes this order.

```python
a = 4
assert a % 2 == 0
``` 

Use failure messages in assertions

```python
assert a % 2 == 0, "value was odd, should be even"
```

Use the following naming convention with test methods:  

test\_\[unit_under_test\]\_\[variables_for_the_test\]\_\[expected_state\]

Example:

```python
def test_add_one_and_one_equals_two():
```