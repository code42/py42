# Getting started with py42

This guide contains information on:

* [Licensing](#licensing)
* [Installation](#installation)
* [Authentication](#authentication)
* [Troubleshooting and Support](#troubleshooting-and-support)

## Licensing

This project uses [MIT License](https://github.com/code42/py42/blob/master/LICENSE.md).

## Installation

There are different ways to install py42. The most common way is to use `pip`:
```bash
pip install py42
```

You can also install from source with these steps:

1. Download the source code from GitHub:
```bash
git clone https://github.com/code42/py42.git
```

2. From the root project directory, run:
```bash
python setup.py sdist
```

3. From the `dist` directory, install using `pip`:
```bash
pip install py42-[VERSION].tar.gz
```

## Authentication

WARNING: Currently, py42 uses token-based authentication only.

To initialize the `py42.sdk.SDK` object, you must use basic auth and provide your credentials. We recommend scripts
using a secure password storage library, such as `keyring`, for retrieving passwords. However, subsequent requests use
JWT authentication.

py42 currently does not support SSO login providers.

## Troubleshooting and Support

**Try turning on debug mode.** Debug mode may be useful if you are trying to determine if you are experiencing
permission issues. When debug mode is on, py42 logs HTTP request URLs and parameters to the console. Use the following
as a guide for how to turn debug mode on in py42:
```python
import py42.sdk
import py42.sdk.settings.debug as debug

py42.sdk.settings.debug.level = debug.DEBUG
```

**File an issue on GitHub.** If you have found an issue with py42, you can create a *New Issue* at the
[project repository](https://github.com/code42/py42/issues). See this
[guide](https://help.github.com/en/github/managing-your-work-on-github/creating-an-issue) for more information.
