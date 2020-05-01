import json

from py42.clients import BaseClient


class ExfiltrationClient(BaseClient):

    _version = u"v1"
    _resource = u"query-endpoint-exfiltration-rule"
    _api_prefix = u"/svc/api/{0}/Rules/{1}".format(_version, _resource)

    def __init__(self, session, tenant_id):
        super(ExfiltrationClient, self).__init__(session)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch exfiltration alert rule by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._tenant_id, u"ruleIds": [rule_id]}
        return self._session.post(self._api_prefix, data=json.dumps(data))
