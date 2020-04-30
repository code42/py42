import json

from py42.clients import BaseClient


class FileTypeMismatchClient(BaseClient):

    _version = u"v1"
    _resource = u"query-file-type-mismatch-rule"
    _api_prefix = u"/svc/api/{0}/Rules/{1}".format(_version, _resource)

    def __init__(self, session, tenant_id):
        super(FileTypeMismatchClient, self).__init__(session)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch File type mismatch alert rules by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {"tenantId": self._tenant_id, "ruleIds": [rule_id]}
        return self._session.post(self._api_prefix, data=json.dumps(data))
