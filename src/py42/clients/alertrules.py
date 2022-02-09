from py42 import settings
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42InvalidRuleOperationError


class AlertRulesClient:
    """`Rest Documentation <https://developer.code42.com/api/#tag/Rules>`__"""

    def __init__(self, alerts_service, alert_rules_service):
        self._alerts_service = alerts_service
        self._alert_rules_service = alert_rules_service

    @property
    def exfiltration(self):
        """A collection of methods for managing exfiltration alert rules.

        Returns:
            :class:`py42.services.alertrules.exfiltration.ExfiltrationService`
        """
        return self._alert_rules_service.exfiltration

    @property
    def cloudshare(self):
        """A collection of methods for managing cloud sharing alert rules.

        Returns:
            :class:`py42.services.alertrules.cloud_share.CloudShareService`
        """
        return self._alert_rules_service.cloudshare

    @property
    def filetypemismatch(self):
        """A collection of methods for managing file type mismatch alert rules.

        Returns:
            :class:`py42.services.alertrules.file_type_mismatch.FileTypeMismatchService`
        """
        return self._alert_rules_service.filetypemismatch

    def add_user(self, rule_id, user_id):
        """Update alert rule criteria to add a user and all their aliases to an alert rule. A rule's
        user list can either be inclusive (only the users on the list can generate alerts) or exclusive
        (everyone can generate alerts, except users on the list). This method will include or
        exclude based on the rule configuration.

        `Rest Documentation <https://developer.code42.com/api/#operation/Rules_AddUsersToRule>`__

        Args:
            rule_id (str): Observer Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to add to the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        try:
            return self._alert_rules_service.add_user(rule_id, user_id)
        except Py42InternalServerError as err:
            rules = self.get_by_observer_id(rule_id)["ruleMetadata"]
            _check_if_system_rule(err, rules)
            raise

    def remove_user(self, rule_id, user_id):
        """Update alert rule criteria to remove a user and all their aliases from an alert rule. A rule's
        user list can either be inclusive (only the users on the list can generate alerts) or exclusive
        (everyone can generate alerts, except users on the list). This method will include or
        exclude based on the rule configuration.

        `Rest Documentation <https://developer.code42.com/api/#operation/Rules_RemoveUsersFromRule>`__

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to remove from the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        try:
            return self._alert_rules_service.remove_user(rule_id, user_id)
        except Py42InternalServerError as err:
            rules = self.get_by_observer_id(rule_id)["ruleMetadata"]
            _check_if_system_rule(err, rules)
            raise

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove all users the from the alert rule.

        `Rest Documentation <https://developer.code42.com/api/#operation/Rules_RemoveAllUsersFromRule>`__

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        try:
            return self._alert_rules_service.remove_all_users(rule_id)
        except Py42InternalServerError as err:
            rules = self.get_by_observer_id(rule_id)["ruleMetadata"]
            _check_if_system_rule(err, rules)
            raise

    def get_page(
        self, sort_key="CreatedAt", sort_direction="DESC", page_num=1, page_size=None
    ):
        """Gets a page of alert rules. Note that you can use page_size here the same
        way as other methods that have a `page_size` parameter in py42. However, under
        the hood, it subtracts one from the given page size in the implementation as
        the Code42 alerts API expected the start page to be zero while the rest of the
        Code42 APIs expect the start page to be one.

        Args:
            sort_key (str, optional): Sort results based by field. Defaults to "CreatedAt".
            sort_direction (str, optional): ``ASC`` or ``DESC``. Constants available at
                :class:`py42.constants.SortDirection`. Defaults to  "DESC".
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

    def get_all(self, sort_key="CreatedAt", sort_direction="DESC"):
        """Fetch all available rules.

        Args:
            sort_key (str, optional): Sort results based by field. Defaults to 'CreatedAt'.
            sort_direction (str, optional): ``ASC`` or ``DESC``. Constants available at
                :class:`py42.constants.SortDirection`. Defaults to  "DESC"

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


def _check_if_system_rule(base_err, rules):
    """You cannot add or remove users from system rules this way; use the specific
    feature behind the rule, such as the Departing Employee list."""
    if rules and rules[0]["isSystem"]:
        observer_id = rules[0]["observerRuleId"]
        source = rules[0]["ruleSource"]
        raise Py42InvalidRuleOperationError(base_err, observer_id, source)
