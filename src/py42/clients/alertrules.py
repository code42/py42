from py42.clients import BaseClient

# Below comments are to discuss design and is not intended to be official documentation.


class AlertRulesClient(BaseClient):
    """
    `add` and `remove_users` require ids, i.e ruleIds and userIds, irrespective of which
    type of rules they belong to, whereas search is dependent on rule type.

    {
      "tenantId": "string",
      "ruleId": "string",
      "userList": [
        {
          "userIdFromAuthority": "string",
          "userAliasList": [
            "string"
          ]
        }
      ]
    }

    {
      "tenantId": "string",
      "ruleId": "string",
      "userIdList": [
        "string"
      ]
    }

    Search create & update have 3 different endpoints for each task, e.g for search
        /api/v1/Rules/query-cloud-share-permissions-rule
        /api/v1/Rules/query-endpoint-exfiltration-rule
        /api/v1/Rules/query-file-type-mismatch-rule

    1. Design it similar to detectionlists
        Now based on future requirement to add/update rules etc,
        We can have module AlertRules and below clients
            CloudShare
            EndpointExfiltration
            FileTypeMismatch

         e.g sdk.alertrules.cloudshare.search(),
             sdk.alertrules.endpointexfiltration.search(),
             sdk.alertrules.filetypemismatch.search(), similarly for add and update.

             sdk.alertrules.add_users(), sdk.alertrules.remove_users(), etc

    2. Create an AlertRulesClient focusing only on current requirement.

        sdk.alertrules.add_users(),
        sdk.alertrules.remove_users(),
        sdk.alertrules.get(): this will internally search for each rule type and combine the results
          and return response.

      This commit contains current changes as per this approach.
    """

    def add_users(self, rule_id, user_ids):
        pass

    def remove_users(self, rule_id, user_ids):
        pass

    def remove_all_users(self, rule_id, user_ids):
        pass

    def _get_cloud_share(self):
        pass

    def _get_endpoint_exfiltration(self):
        pass

    def _get_file_type_mismatch(self):
        pass

    def get(self, rule_id):
        pass

    def get_by_name(self, rule_name):
        pass
