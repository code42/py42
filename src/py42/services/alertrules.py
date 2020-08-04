import json

from py42.services import BaseClient


class AlertRulesService(BaseClient):
    """A client to manage Alert Rules."""

    _version = u"v1"
    _resource = u"Rules/"
    _api_prefix = u"/svc/api/{}/{}".format(_version, _resource)

    def __init__(self, connection, user_context, detection_list_user_client):
        super(AlertRulesService, self).__init__(connection)
        self._user_context = user_context
        self._detection_list_user_client = detection_list_user_client
        self._exfiltration = None
        self._cloud_share = None
        self._file_type_mismatch = None

    @property
    def exfiltration(self):
        if not self._exfiltration:
            tenant_id = self._user_context.get_current_tenant_id()
            self._exfiltration = ExfiltrationClient(self._connection, tenant_id)
        return self._exfiltration

    @property
    def cloudshare(self):
        if not self._cloud_share:
            tenant_id = self._user_context.get_current_tenant_id()
            self._cloud_share = CloudShareClient(self._connection, tenant_id)
        return self._cloud_share

    @property
    def filetypemismatch(self):
        if not self._file_type_mismatch:
            self._file_type_mismatch = FileTypeMismatchClient(
                self._connection, self._tenant_id
            )
        return self._file_type_mismatch

    def add_user(self, rule_id, user_id):
        tenant_id = self._user_context.get_current_tenant_id()
        user_details = self._detection_list_user_client.get_by_id(user_id)
        user_aliases = user_details["cloudUsernames"] or []
        data = {
            u"tenantId": tenant_id,
            u"ruleId": rule_id,
            u"userList": [
                {u"userIdFromAuthority": user_id, u"userAliasList": user_aliases}
            ],
        }
        uri = u"{}{}".format(self._api_prefix, u"add-users")
        return self._connection.post(uri, data=json.dumps(data))

    def remove_user(self, rule_id, user_id):
        user_ids = [user_id]
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id, u"userIdList": user_ids}
        uri = u"{}{}".format(self._api_prefix, u"remove-users")
        return self._connection.post(uri, data=json.dumps(data))

    def remove_all_users(self, rule_id):
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id}
        uri = u"{}{}".format(self._api_prefix, u"remove-all-users")
        return self._connection.post(uri, data=json.dumps(data))


class CloudShareClient(BaseClient):

    _version = u"v1"
    _resource = u"query-cloud-share-permissions-rule"
    _api_prefix = u"/svc/api/{}/Rules/{}".format(_version, _resource)

    def __init__(self, connection, tenant_id):
        super(CloudShareClient, self).__init__(connection)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch cloud share alert rule by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._tenant_id, u"ruleIds": [rule_id]}
        return self._connection.post(self._api_prefix, data=json.dumps(data))


class ExfiltrationClient(BaseClient):

    _version = u"v1"
    _resource = u"query-endpoint-exfiltration-rule"
    _api_prefix = u"/svc/api/{}/Rules/{}".format(_version, _resource)

    def __init__(self, connection, tenant_id):
        super(ExfiltrationClient, self).__init__(connection)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch exfiltration alert rule by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._tenant_id, u"ruleIds": [rule_id]}
        return self._connection.post(self._api_prefix, data=json.dumps(data))


class FileTypeMismatchClient(BaseClient):

    _version = u"v1"
    _resource = u"query-file-type-mismatch-rule"
    _api_prefix = u"/svc/api/{}/Rules/{}".format(_version, _resource)

    def __init__(self, connection, tenant_id):
        super(FileTypeMismatchClient, self).__init__(connection)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch File type mismatch alert rules by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {"tenantId": self._tenant_id, "ruleIds": [rule_id]}
        return self._connection.post(self._api_prefix, data=json.dumps(data))
