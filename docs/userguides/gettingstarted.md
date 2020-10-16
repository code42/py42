# Getting started with py42

* [Licensing](#licensing)
* [Installation](#installation)
* [Authentication](#authentication)
* [Troubleshooting and Support](#troubleshooting-and-support)

## Licensing

This project uses the [MIT License](https://github.com/code42/py42/blob/master/LICENSE.md).

## Installation

You can install py42 from PyPI, from source, or from distribution.

### From PyPI

The easiest and most common way is to use `pip`:

```bash
pip install py42
```

To install a previous version of py42 via `pip`, add the version number. For example, to install version
0.4.1, you would enter:

```bash
pip install py42==0.4.1
```

Visit the [project history](https://pypi.org/project/py42/#history) on PyPI to see all published versions.

### From source

Alternatively, you can install py42 directly from [source code](https://github.com/code42/py42):

```bash
git clone https://github.com/code42/py42.git
```

When it finishes downloading, from the root project directory, run:

```bash
python setup.py install
```

### From distribution

If you want create a `.tar` ball for installing elsewhere, run this command from the project's root directory:

```bash
python setup.py sdist
```

After it finishes building, the `.tar` ball will be located in the newly created `dist` directory. To install it, enter:

```bash
pip install py42-[VERSION].tar.gz
```

## Authentication

```eval_rst
.. important:: py42 currently only supports token-based authentication.
```

To initialize the `py42.sdk.SDKClient`, you must provide your credentials (basic authentication). If you are writing a script,
we recommend using a secure password storage library, such as `keyring`, for retrieving passwords. However, subsequent
requests use JWT authentication.

If your account uses [two-factor authentication](https://support.code42.com/Administrator/Cloud/Configuring/Two-factor_authentication_for_local_users), include the time-based one-time password (TOTP) when you initialize the `py42.sdk.SDKClient`.
You can also provide a callable object that returns a TOTP. If you pass a callable, it will be called whenever a new TOTP is required to renew the authentication token.

py42 currently does **not** support SSO login providers or any other identity providers such as Active Directory or
Okta.

## Troubleshooting and support

### Debug mode

Debug mode may be useful if you are trying to determine if you are experiencing permissions issues. When debug mode is
on, py42 logs HTTP request data to the console's stderr. Use the following as a guide for how to turn on debug mode in
py42:

```python
import py42.sdk
import py42.settings
import logging

py42.settings.debug.level = logging.DEBUG
```

To provide your own logger, just replace `py42.settings.debug.logger`:

```
custom_logger = logging.getLogger("my_app")
handler = logging.FileHandler("my_app.log")
custom_logger.addHandler(handler)

py42.settings.debug.logger = custom_logger
```

### File an issue on GitHub

If you are experiencing an issue with py42, you can create a *New issue* at the
[project repository](https://github.com/code42/py42/issues). See the Github [guide on creating an issue](https://help.github.com/en/github/managing-your-work-on-github/creating-an-issue) for more information.

### Contact Code42 Support

If you don't have a GitHub account and are experiencing issues, contact
[Code42 support](https://support.code42.com/).

## What's next?

Learn the basics by following the py42 [Basics guide](basics.md).
