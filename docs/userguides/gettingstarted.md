# Getting started with py42

This guide contains information on:

* [Licensing](#licensing)
* [Installation](#installation)
* [Authentication](#authentication)
* [Troubleshooting and Support](#troubleshooting-and-support)

## Licensing

This project uses the [MIT License](https://github.com/code42/py42/blob/master/LICENSE.md).

## Installation

There are different ways to install py42. The easiest and most common way is to use `pip`:
```bash
pip install py42
```

If you need to install a previous version of py42, you can specify the version with `pip`. For example, if you want to
install version 0.4.1, you would do this:
```bash
pip install py42==0.4.1
```

Visit the [project history](https://pypi.org/project/py42/#history) on PyPI too see all published versions.

You can also install from source with these steps:

1. Download the source code from GitHub:
```bash
git clone https://github.com/code42/py42.git
```

2. Fro the root project directory, run:
```bash
python setup.py install
```

If you want create a tarbar for installing elsewhere, follow these steps:

1. From the root project directory, run:
```bash
python setup.py sdist
```

The tarbar is in the newly created `dist` directory. To install it, do:
```bash
pip install py42-[VERSION].tar.gz
```

## Authentication

```eval_rst
.. important:: Currently, py42 uses token-based authentication only.
```

To initialize the `py42.sdk.SDK` object, you must provide your credentials (basic auth). If you are writing a script,
we recommend using a secure password storage library, such as `keyring`, for retrieving passwords. However, subsequent
requests use JWT authentication.

py42 currently does **not** support SSO login providers or any other Identity providers such Active Directory or Okta.

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

**Reach out to Code42 Support.** If you don't have a GitHub account and are experiencing an issue, reach out to
[Code42 support](https://support.code42.com/).


### What's Next?

Learn the basics by following the py42 [basics guide](basics.html).
