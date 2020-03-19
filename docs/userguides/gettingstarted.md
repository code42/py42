# Getting started with py42

This guide contains information on:

* [Licensing](#licensing)
* [Installation](#installation)
* [Authentication](#authentication)
* [Troubleshooting and Support](#troubleshooting-and-support)

## Licensing

Please observe our license agreement:

    MIT License

    Copyright (c) 2020 Code42 Software

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

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
