# Contributing to the Code42 Python SDK

## Development environment

Install py42 and its development dependencies. The "-e" option installs py42 in ["editable mode"](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs). 

```bash
pip install -e .[dev]
```

If you are using Z shell (zsh), you may need to escape the brackets.

## General

### Do

* Use positional argument specifiers in `str.format()`

## Wrapping web APIs

### Do

* Name the method starting with a verb
* Specify required arguments as positional arguments
* Specify optional arguments as keyword arguments
* Include `**kwargs` as the last parameter
* Use the newest supported implementation (e.g. v4 instead of v1, even if a related API only has a v1 implementation)

## Changes

### Do

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

## Documentation

Public functions, classes, and methods should have docstrings. Follow [Google's format](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Generating documentation

py42 uses [Sphinx](http://www.sphinx-doc.org/) to generate documentation.

To build the documentation, run the following from the `docs` directory:

```bash
make html
```

To view the resulting documentation, open `docs/_build/html/index.html`.
