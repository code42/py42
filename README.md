# Code42 Python SDK

## Requirements
- Python 2.7.x
- [requests](http://docs.python-requests.org/en/master/)
- Code42 Server 6.5.x

## Usage
```python
from code42.sdk import SDKClient

sdk = SDKClient.create_from_local_logon("https://example.code42.com", "foo", "bar")
authority_api = sdk.authority_api
```

## Configuration

**code42/lib/http/settings.py** defines default settings. To override them, import the settings and override values as
necessary before creating the client. For example, to disable certificate validation in a dev environment: 

```python
#...
import code42.lib.http.settings as settings
#...
settings.verify_ssl_certs = False
sdk = SDKClient.create_from_local_logon(host, username, password)
```
