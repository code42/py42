# Contributing to py42

## Set up your Development environment

The very first thing to do is to clone the py42 repo and make it your working directory!

```bash
git clone https://github.com/code42/py42
cd py42
```

To set up your development environment, create a python virtual environment and activate it. This keeps your dependencies sandboxed so that they are unaffected by (and do not affect) other python packages you may have installed. There are many ways to do this, but we recommend using [pyenv](https://github.com/pyenv/pyenv).

Install `pyenv` and `pyenv-virtualenv` via [homebrew](https://brew.sh/):

```bash
brew install pyenv pyenv-virtualenv
```

After installing `pyenv` and `pyenv-virtualenv`, be sure to add the following entries to your `.zshrc` (or `.bashrc` if you are using bash) and restart your shell:

```bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Then, create your virtual environment. While py42 runs on python 2.7 and 3.5+, a 3.6+ version is required for development in order to run all of the unit tests and style checks.

```bash
$ pyenv install 3.6.10
$ pyenv virtualenv 3.6.10 py42
$ pyenv activate py42
```

Use `source deactivate` to exit the virtual environment and `pyenv activate py42` to reactivate it.


Next, with your virtual environment activated, install py42 and its development dependencies. The `-e` option installs py42 in
["editable mode"](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).

```bash
$ pip install -e .[dev]
```

Open the project in your IDE of choice and change the python environment to
point to your virtual environment, and you should be ready to go!

## General

* Use positional argument specifiers in `str.format()`
* Use syntax and built-in modules that are compatible with both Python 2 and 3.
* Use the `py42._internal.compat` module to create abstractions around functionality that differs between 2 and 3.

## Wrapping web APIs

* Name the method starting with a verb
* Specify required arguments as positional arguments
* Specify optional arguments as keyword arguments

## Changes

Document all notable consumer-affecting changes in CHANGELOG.md per principles and guidelines at
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Tests

We use [tox](https://tox.readthedocs.io/en/latest/#) to run the
[pytest](https://docs.pytest.org/) test framework on Python 2.7, 3.5, 3.6, 3.7, and 3.8.

Run the below at the root of the repo to run the tests on all versions of python
that are available within your PATH.

```bash
$ tox
```

This will also test that the documentation build passes.

### Writing tests

Put actual before expected values in assert statements. Pytest assumes this order.

```python
a = 4
assert a % 2 == 0
```

Use the following naming convention with test methods:

test\_\[unit_under_test\]\_\[variables_for_the_test\]\_\[expected_state\]

Example:

```python
def test_add_one_and_one_equals_two():
```

## Documentation

Public functions, classes, and methods should have docstrings.
Follow [Google's format](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Generating documentation

py42 uses [Sphinx](http://www.sphinx-doc.org/) to generate documentation.

To build the documentation, run the following from the `docs` directory:

```bash
make html
```

To view the resulting documentation, open `docs/_build/html/index.html`.

For the best viewing experience, run a local server to view the documentation.
You can this by running the below from the `docs` directory using python 3:

```bash
python -m http.server --directory "_build/html" 1337
```

and then pointing your browser to `localhost:1337`.
