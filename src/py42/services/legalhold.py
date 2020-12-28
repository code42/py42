from py42 import settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42Error
from py42.exceptions import Py42ForbiddenError
from py42.exceptions import Py42LegalHoldCriteriaMissingError
from py42.exceptions import Py42LegalHoldNotFoundOrPermissionDeniedError
from py42.exceptions import Py42UserAlreadyAddedError
from py42.services import BaseService
from py42.services.util import get_all_pages


def _active_state_map(active):
    _map = {True: u"ACTIVE", False: u"INACTIVE", None: u"ALL"}
    try:
        return _map[active]
    except KeyError:
        raise Py42Error(
            "Invalid argument: '{}'. active must be True, False, or None".format(active)
        )


class LegalHoldService(BaseService):
    """A service for interacting with Code42 Legal Hold APIs.

    The LegalHoldService provides the ability to manage Code42 Legal Hold Policies and Matters.
    It can:
    - Create, view, and list all existing Policies.
    - Create, view, deactivate, reactivate, and list all existing Matters.
    - Add/remove Custodians from a Matter.
    """

    def create_policy(self, name, policy=None):
        """Creates a new Legal Hold Preservation Policy.
        `V4 REST Documentation <https://console.us.code42.com/swagger/#/legal-hold-policy/LegalHoldPolicy_Create>`__

        Args:
            name (str): The name of the new Policy.
            policy (dict, optional): The desired Preservation Policy settings as a dict. Defaults to
                None (where the server-default backup set is used).

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v4/legal-hold-policy/create"
        data = {u"name": name, u"policy": policy}
        return self._connection.post(uri, json=data)

    def create_matter(
        self, name, hold_policy_uid, description=None, notes=None, hold_ext_ref=None
    ):
        """Creates a new, active Legal Hold Matter.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHold-post>`__

        Args:
            name (str): The name of the new Legal Hold Matter.
            hold_policy_uid (str): The identifier of the Preservation Policy that will apply to this
                Matter.
            description (str, optional): An optional description of the Matter. Defaults to None.
            notes (str, optional): Optional notes information. Defaults to None.
            hold_ext_ref (str, optional): Optional external reference information. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/LegalHold"
        data = {
            u"name": name,
            u"holdPolicyUid": hold_policy_uid,
            u"description": description,
            u"notes": notes,
            u"holdExtRef": hold_ext_ref,
        }
        return self._connection.post(uri, json=data)

    def get_policy_by_uid(self, legal_hold_policy_uid):
        """Gets a single Preservation Policy.
        `V4 REST Documentation <https://console.us.code42.com/swagger/#/legal-hold-policy/LegalHoldPolicy_View>`__

        Args:
            legal_hold_policy_uid (str): The identifier of the Preservation Policy.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the Policy.
        """
        uri = u"/api/v4/legal-hold-policy/view"
        params = {u"legalHoldPolicyUid": legal_hold_policy_uid}
        return self._connection.get(uri, params=params)

    def get_policy_list(self):
        """Gets a list of existing Preservation Policies.
        `V4 REST Documentation <https://console.us.code42.com/swagger/#/legal-hold-policy/LegalHoldPolicy_List>`__

        Returns:
            :class:`py42.response.Py42Response`: A response containing the list of Policies.
        """
        uri = u"/api/v4/legal-hold-policy/list"
        return self._connection.get(uri)

    def get_matter_by_uid(self, legal_hold_uid):
        """Gets a single Legal Hold Matter.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHold-get>`__

        Args:
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the Matter.
        """
        uri = u"/api/LegalHold/{}".format(legal_hold_uid)
        try:
            return self._connection.get(uri)
        except Py42ForbiddenError as err:
            raise Py42LegalHoldNotFoundOrPermissionDeniedError(err, legal_hold_uid)

    def get_matters_page(
        self,
        page_num,
        creator_user_uid=None,
        active=True,
        name=None,
        hold_ext_ref=None,
        page_size=None,
    ):
        """Gets a page of existing Legal Hold Matters.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHold-get>`__

        Args:
            page_num (int): The page number to request.
            creator_user_uid (str, optional): Find Matters by the identifier of the user who created
                them. Defaults to None.
            active (bool or None, optional): Find Matters by their active state. True returns
                active Matters, False returns inactive Matters, None returns all Matters regardless
                of state. Defaults to True.
            name (str, optional): Find Matters with a 'name' that either equals or contains
                this value. Defaults to None.
            hold_ext_ref (str, optional): Find Matters having a matching external reference field.
                Defaults to None.
            page_size (int, optional): The number of legal hold items to return per page.
                Defaults to `py42.settings.items_per_page`.

        Returns:
            :class:`py42.response.Py42Response`:
        """

        active_state = _active_state_map(active)
        page_size = page_size or settings.items_per_page
        uri = u"/api/LegalHold"
        params = {
            u"creatorUserUid": creator_user_uid,
            u"activeState": active_state,
            u"name": name,
            u"holdExtRef": hold_ext_ref,
            u"pgNum": page_num,
            u"pgSize": page_size,
        }
        return self._connection.get(uri, params=params)

    def get_all_matters(
        self, creator_user_uid=None, active=True, name=None, hold_ext_ref=None
    ):
        """Gets all existing Legal Hold Matters.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHold-get>`__

        Args:
            creator_user_uid (str, optional): Find Matters by the identifier of the user who created
                them. Defaults to None.
            active (bool or None, optional): Find Matters by their active state. True returns
                active Matters, False returns inactive Matters, None returns all Matters regardless
                of state. Defaults to True.
            name (str, optional): Find Matters with a 'name' that either equals or contains
                this value. Defaults to None.
            hold_ext_ref (str, optional): Find Matters having a matching external reference field.
                Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of Legal Hold Matters.
        """
        return get_all_pages(
            self.get_matters_page,
            u"legalHolds",
            creator_user_uid=creator_user_uid,
            active=active,
            name=name,
            hold_ext_ref=hold_ext_ref,
        )

    def get_custodians_page(
        self,
        page_num,
        legal_hold_membership_uid=None,
        legal_hold_uid=None,
        user_uid=None,
        user=None,
        active=True,
        page_size=None,
    ):
        """Gets an individual page of Legal Hold memberships. One of the following
        optional args is required to determine which custodians to retrieve:

        `legal_hold_membership_uid`, `legal_hold_uid`, `user_uid`, `user`

        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHoldMembership-get>`__

        Args:
            page_num (int): The page number to request.
            legal_hold_membership_uid (str, optional): Find LegalHoldMemberships with a
                specific membership UID. Defaults to None.
            legal_hold_uid (str, optional): Find LegalHoldMemberships for the Legal Hold Matter
                with this unique identifier. Defaults to None.
            user_uid (str, optional): Find LegalHoldMemberships for the user with this identifier.
                Defaults to None.
            user (str, optional): Find LegalHoldMemberships by flexibly searching on username,
                email, extUserRef, or last name. Will find partial matches. Defaults to None.
            active (bool or None, optional): Find LegalHoldMemberships by their active state. True
                returns active LegalHoldMemberships, False returns inactive LegalHoldMemberships,
                None returns all LegalHoldMemberships regardless of state. Defaults to True.
            page_size (int, optional): The size of the page. Defaults to `py42.settings.items_per_page`.

        Returns:
            :class:`py42.response.Py42Response`:
        """
        active_state = _active_state_map(active)
        page_size = page_size or settings.items_per_page
        params = {
            u"legalHoldMembershipUid": legal_hold_membership_uid,
            u"legalHoldUid": legal_hold_uid,
            u"userUid": user_uid,
            u"user": user,
            u"activeState": active_state,
            u"pgNum": page_num,
            u"pgSize": page_size,
        }
        uri = u"/api/LegalHoldMembership"
        try:
            return self._connection.get(uri, params=params)
        except Py42BadRequestError as ex:
            if u"At least one criteria must be specified" in ex.response.text:
                raise Py42LegalHoldCriteriaMissingError(ex)
            raise

    def get_all_matter_custodians(
        self, legal_hold_uid=None, user_uid=None, user=None, active=True
    ):
        """Gets all Legal Hold memberships.

        Each user (Custodian) who has been added to a Legal Hold Matter is returned by the server as
        a LegalHoldMembership object in the response body.  If the object's active state is
        "INACTIVE", they have been removed from the Matter and are no longer subject to the Legal
        Hold retention rules. Users can be Custodians of multiple Legal Holds at once (and thus
        would be part of multiple LegalHoldMembership objects).
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHoldMembership-get>`__

        Args:
            legal_hold_uid (str, optional): Find LegalHoldMemberships for the Legal Hold Matter
                with this unique identifier. Defaults to None.
            user_uid (str, optional): Find LegalHoldMemberships for the user with this identifier.
                Defaults to None.
            user (str, optional): Find LegalHoldMemberships by flexibly searching on username,
                email, extUserRef, or last name. Will find partial matches. Defaults to None.
            active (bool or None, optional): Find LegalHoldMemberships by their active state. True
                returns active LegalHoldMemberships, False returns inactive LegalHoldMemberships,
                None returns all LegalHoldMemberships regardless of state. Defaults to True.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of LegalHoldMembership objects.
        """
        return get_all_pages(
            self.get_custodians_page,
            u"legalHoldMemberships",
            legal_hold_uid=legal_hold_uid,
            user_uid=user_uid,
            user=user,
            active=active,
        )

    def add_to_matter(self, user_uid, legal_hold_uid):
        """Add a user (Custodian) to a Legal Hold Matter.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHoldMembership-post>`__

        Args:
            user_uid (str): The identifier of the user.
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/LegalHoldMembership"
        data = {u"legalHoldUid": legal_hold_uid, u"userUid": user_uid}
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as err:
            if u"USER_ALREADY_IN_HOLD" in err.response.text:
                matter = self.get_matter_by_uid(legal_hold_uid)
                matter_id_and_name_text = u"legal hold matter id={}, name={}".format(
                    legal_hold_uid, matter[u"name"]
                )
                raise Py42UserAlreadyAddedError(err, user_uid, matter_id_and_name_text)
            raise

    def remove_from_matter(self, legal_hold_membership_uid):
        """Remove a user (Custodian) from a Legal Hold Matter.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHoldMembershipDeactivation-post>`__

        Args:
            legal_hold_membership_uid (str): The identifier of the LegalHoldMembership representing
                the Custodian to Matter relationship.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/LegalHoldMembershipDeactivation"
        data = {u"legalHoldMembershipUid": legal_hold_membership_uid}
        return self._connection.post(uri, json=data)

    def deactivate_matter(self, legal_hold_uid):
        """Deactivates and closes a Legal Hold Matter.
        `V4 REST Documentation <https://console.us.code42.com/swagger/#/legal-hold-deactivation/LegalHoldDeactivation_Update>`__

        Args:
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v4/legal-hold-deactivation/update"
        data = {u"legalHoldUid": legal_hold_uid}
        return self._connection.post(uri, json=data)

    def reactivate_matter(self, legal_hold_uid):
        """Reactivates and re-opens a closed Matter.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#LegalHoldReactivation-put>`__

        Args:
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/LegalHoldReactivation/{}".format(legal_hold_uid)
        return self._connection.put(uri)
