from py42 import settings


class AlertRulesModule(object):
    def __init__(self, alerts_service, alert_rules_service):
        self._alerts_service = alerts_service
        self._alert_rules_service = alert_rules_service

    @property
    def exfiltration(self):
        """A collection of methods for managing exfiltration alert rules.

        Returns:
            :class:`py42.services.alertrules.exfiltration.ExfiltrationClient`
        """
        return self._alert_rules_service.exfiltration

    @property
    def cloudshare(self):
        """A collection of methods for managing cloud sharing alert rules.

        Returns:
            :class:`py42.services.alertrules.cloud_share.CloudShareClient`
        """
        return self._alert_rules_service.cloudshare

    @property
    def filetypemismatch(self):
        """A collection of methods for managing file type mismatch alert rules.

        Returns:
            :class:`py42.services.alertrules.file_type_mismatch.FileTypeMismatchClient`
        """
        return self._alert_rules_service.filetypemismatch

    def add_user(self, rule_id, user_id):
        """Update alert rule to monitor user aliases against the Uid for the given rule id.

        Args:
            rule_id (str): Observer Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to add to the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._alert_rules_service.add_user(rule_id, user_id)

    def remove_user(self, rule_id, user_id):
        """Update alert rule criteria to remove a user and all its aliases from a rule.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to remove from the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._alert_rules_service.remove_user(rule_id, user_id)

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove all users the from the alert rule.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        rules_client = self.microservice_client_factory.get_alert_rules_client()
        return rules_client.remove_all_users(rule_id)

    def get_page(
        self, sort_key=u"CreatedAt", sort_direction=u"DESC", page_num=1, page_size=None
    ):
        """Gets a page of alert rules. Note that you can use page_size here the same
        way as other methods that have a `page_size` parameter in py42. However, under
        the hood, it subtracts one from the given page size in the implementation as
        the Code42 alerts API expected the start page to be zero while the rest of the
        Code42 APIs expect the start page to be one.

        sort_key (str, optional): Sort results based by field. Defaults to "CreatedAt".
        sort_direction (str, optional): ``ASC`` or ``DESC``. Defaults to  "DESC".
        page_num (int, optional): The page number to get. Defaults to 1.
        page_size (int, optional): The number of items per page. Defaults to `py42.settings.items_per_page`.

        Returns:
             :class:`py42.response.Py42Response`
        """
        page_size = page_size or settings.items_per_page
        return self._alerts_service.get_rules_page(
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_num=page_num,
            page_size=page_size,
        )

    def get_all(self, sort_key=u"CreatedAt", sort_direction=u"DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str, optional): Sort results based by field. Defaults to 'CreatedAt'.
            sort_direction (str, optional): ``ASC`` or ``DESC``. Defaults to  "DESC"

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of rules.
        """
        return self._alerts_service.get_all_rules(
            sort_key=sort_key, sort_direction=sort_direction
        )

    def get_all_by_name(self, rule_name):
        """Search for matching rules by name.

        Args:
            rule_name (str): Rule name to search for, case insensitive search.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of rules with the given name.
        """
        return self._alerts_service.get_all_rules_by_name(rule_name)

    def get_by_observer_id(self, observer_id):
        """Get the rule with the matching observer ID.

        Args:
            observer_id (str): The observer ID of the rule to return.

        Returns
            :class:`py42.response.Py42Response`
        """
        return self._alerts_service.get_rule_by_observer_id(observer_id)
