import json
from py42.clients import BaseClient
from py42.clients.util import get_all_pages


_ALERT_RULE_ENDPOINTS = {
    "exfiltration": u"query-endpoint-exfiltration-rule",
    "cloudshare": u"query-cloud-share-permissions-rule",
    "typemismatch": u"query-file-type-mismatch-rule",
}


class AlertRulesClient(BaseClient):
    """A client to manage Alert Rules."""

    _version = u"v1"
    _resource = u"Rules/"
    _api_prefix = u"/svc/api/{0}/".format(_version)

    def __init__(self, session, user_context):
        super(AlertRulesClient, self).__init__(session)
        self._user_context = user_context

    def add_user(self, rule_id, user_id, user_aliases):
        """Update alert rule criteria to apply the rule for specific user(s) for the given rule id.

        Args:
            rule_id (str): Id of a rule to be updated.
            user_id (str): User id who needs to be added to the criteria.
            user_aliases (str): Email ids/Aliases who needs to be added to criteria.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {
            u"tenantId": tenant_id,
            u"ruleId": rule_id,
            u"userList": [
                {
                    # not sure what should be passed here and its significance.
                    u"userIdFromAuthority": user_id,
                    u"userAliasList": [user_aliases],
                }
            ],
        }
        uri = u"{0}{1}{2}".format(self._api_prefix, self._resource, u"add-users")
        return self._session.post(uri, data=json.dumps(data))

    def remove_users(self, rule_id, user_ids):
        """Update alert rule criteria to remove user criteria from the rule.

        Args:
            rule_id (str): Id of a rule to be updated.
            user_ids (str): List of comma separated user ids who needs to be added to the criteria.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id, u"userIdList": [user_ids]}
        uri = u"{0}{1}{2}".format(self._api_prefix, self._resource, u"remove-users")
        return self._session.post(uri, data=json.dumps(data))
        pass

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove the criteria of all users from the rule.

        Args:
            rule_id (str): Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id}
        uri = u"{0}{1}{2}".format(self._api_prefix, self._resource, u"remove-all-users")
        return self._session.post(uri, data=json.dumps(data))

    def get(self, rule_id, rule_type):
        """Fetch alert rules by rule id.

        Args:
            rule_id (str): Id of a rule to be updated.
            rule_type (str): Either of 'exfiltration', 'cloudshare', 'typemismatch' where
              'exfiltration' implies rules related to movement of files,
              'cloudshare' implies rules related to sharing/providing public access to files
              'typemismatch' implies rules related to content and file extension mismatch.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {"tenantId": tenant_id, "ruleIds": [rule_id]}
        uri = u"{0}{1}{2}".format(
            self._api_prefix, self._resource, _ALERT_RULE_ENDPOINTS[rule_type]
        )
        return self._session.post(uri, data=json.dumps(data))

    def _get_alert_rules(
        self, tenant_id, sort_key=None, sort_direction=None, page_num=None, page_size=None
    ):
        data = {
            "tenantId": tenant_id,
            "groups": [],
            "groupClause": "AND",
            "pgNum": page_num,
            "pgSize": page_size,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        resource = u"rules/"
        uri = u"{0}{1}{2}".format(self._api_prefix, resource, u"query-rule-metadata")
        return self._session.post(uri, data=json.dumps(data))

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        tenant_id = self._user_context.get_current_tenant_id()
        return get_all_pages(
            self._get_alert_rules,
            u"items",
            tenant_id=tenant_id,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_by_name(self, rule_name):
        pass
