# Getting started with py42

This guide contains information on:

* [Licensing](#licensing)
* [Installation](#installation)
* [Authentication](#authentication)
* [Troubleshooting and Support](#troubleshooting-and-support)

## Licensing

This project uses MIT License. [Here is more information](https://github.com/code42/py42/blob/master/LICENSE.md).


## Installation

There are different ways to install py42. The most common way would be to use `pip`:
```bash
pip install py42
```

You can also download from source by following these steps:

First, from the root project directory, do:
```bash
python setup.py sdist
```

Then, from the `dist` directory, do:
```bash
pip install py42-[VERSION].tar.gz
```

## Authentication

WARNING: Currently, py42 uses token-based authentication only.
To initialize the SDK, you provide your credentials (basic auth). Subsequent requests use JWT authentication.
py42 currently does not support SSO login providers.

## Troubleshooting and Support

### Upgrading

To upgrade, do:
```bash
pip install py42 --upgrade
```

If you are getting errors after upgrading, try uninstalling and reinstalling:
```bash
pip uninstall py42
pip install py42
```
