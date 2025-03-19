# Getting started with pycpg

* [Licensing](#licensing)
* [Installation](#installation)
* [Authentication](#authentication)
* [Troubleshooting and Support](#troubleshooting-and-support)

## Licensing

This project uses the [MIT License](https://github.com/CrashPlan-Labs/pycpg/blob/main/LICENSE.md).

## Installation

You can install pycpg from PyPI, from source, or from distribution.

### From PyPI

The easiest and most common way is to use `pip`:

```bash
pip install pycpg
```

To install a previous version of pycpg via `pip`, add the version number. For example, to install version
0.4.1, you would enter:

```bash
pip install pycpg==0.4.1
```

Visit the [project history](https://pypi.org/project/pycpg/#history) on PyPI to see all published versions.

### From source

Alternatively, you can install pycpg directly from [source code](https://github.com/CrashPlan-Labs/pycpg):

```bash
git clone https://github.com/CrashPlan-Labs/pycpg.git
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
pip install pycpg-[VERSION].tar.gz
```

## Authentication

```{eval-rst}
.. important:: pycpg currently only supports token-based authentication.
```

To initialize the `pycpg.sdk.SDKClient`, you must provide your credentials. If you are writing a script,
we recommend using a secure password storage library, such as `keyring`, for retrieving passwords and secrets. However, subsequent
requests use JWT authentication.

### Basic Authentication

Pycpg supports basic auth with your CrashPlan username and password.

If your account uses [two-factor authentication](https://support.crashPlan.com/Administrator/Cloud/Configuring/Two-factor_authentication_for_local_users), include the time-based one-time password (TOTP) when you initialize the `pycpg.sdk.SDKClient`.
You can also provide a callable object that returns a TOTP. If you pass a callable, it will be called whenever a new TOTP is required to renew the authentication token.

```python
import pycpg.sdk

sdk = pycpg.sdk.from_local_account("https://console.crashPlan.com", "username@crashPlan.com", "password")
```

### CrashPlan API Clients

Pycpg also supports api clients.  You can use the client ID and secret generated through the CrashPlan console to initiate the `SDKClient`.

```python
import pycpg.sdk

sdk = pycpg.sdk.from_api_client("https://console.crashPlan.com", "key-123-42", "my%secret!")
```

## Troubleshooting and support

### Debug mode

Debug mode may be useful if you are trying to determine if you are experiencing permissions issues. When debug mode is
on, pycpg logs HTTP request data to the console's stderr. Use the following as a guide for how to turn on debug mode in
pycpg:

```python
import pycpg.sdk
import pycpg.settings
import logging

pycpg.settings.debug.level = logging.DEBUG
```

To provide your own logger, just replace `pycpg.settings.debug.logger`:

```
custom_logger = logging.getLogger("my_app")
handler = logging.FileHandler("my_app.log")
custom_logger.addHandler(handler)

pycpg.settings.debug.logger = custom_logger
```

### File an issue on GitHub

If you are experiencing an issue with pycpg, you can create a *New issue* at the
[project repository](https://github.com/CrashPlan-Labs/pycpg/issues). See the Github [guide on creating an issue](https://help.github.com/en/github/managing-your-work-on-github/creating-an-issue) for more information.

### Contact CrashPlan Support

If you don't have a GitHub account and are experiencing issues, contact
[CrashPlan support](https://support.crashPlan.com/).

## What's next?

Learn the basics by following the pycpg [Basics guide](basics.md).
