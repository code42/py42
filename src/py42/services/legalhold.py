from py42 import settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42Error
from py42.exceptions import Py42ForbiddenError
from py42.exceptions import Py42LegalHoldCriteriaMissingError
from py42.exceptions import Py42LegalHoldNotFoundOrPermissionDeniedError
from py42.exceptions import Py42UserAlreadyAddedError
from py42.services import BaseService
from py42.services.util import get_all_pages
from py42.util import parse_timestamp_to_milliseconds_precision


def _active_state_map(active):
    _map = {True: "ACTIVE", False: "INACTIVE", None: "ALL"}
    try:
        return _map[active]
    except KeyError:
        raise Py42Error(
            f"Invalid argument: '{active}'. active must be True, False, or None"
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

        Args:
            name (str): The name of the new Policy.
            policy (dict, optional): The desired Preservation Policy settings as a dict. Defaults to
                None (where the server-default backup set is used).

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v4/legal-hold-policy/create"
        data = {"name": name, "policy": policy}
        return self._connection.post(uri, json=data)

    def create_matter(
        self, name, hold_policy_uid, description=None, notes=None, hold_ext_ref=None
    ):
        """Creates a new, active Legal Hold Matter.

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
        uri = "/api/v1/LegalHold"
        data = {
            "name": name,
            "holdPolicyUid": hold_policy_uid,
            "description": description,
            "notes": notes,
            "holdExtRef": hold_ext_ref,
        }
        return self._connection.post(uri, json=data)

    def get_policy_by_uid(self, legal_hold_policy_uid):
        """Gets a single Preservation Policy.

        Args:
            legal_hold_policy_uid (str): The identifier of the Preservation Policy.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the Policy.
        """
        uri = "/api/v4/legal-hold-policy/view"
        params = {"legalHoldPolicyUid": legal_hold_policy_uid}
        return self._connection.get(uri, params=params)

    def get_policy_list(self):
        """Gets a list of existing Preservation Policies.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the list of Policies.
        """
        uri = "/api/v4/legal-hold-policy/list"
        return self._connection.get(uri)

    def get_matter_by_uid(self, legal_hold_uid):
        """Gets a single Legal Hold Matter.

        Args:
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the Matter.
        """
        uri = f"/api/v1/LegalHold/{legal_hold_uid}"
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
        uri = "/api/v1/LegalHold"
        params = {
            "creatorUserUid": creator_user_uid,
            "activeState": active_state,
            "name": name,
            "holdExtRef": hold_ext_ref,
            "pgNum": page_num,
            "pgSize": page_size,
        }
        return self._connection.get(uri, params=params)

    def get_all_matters(
        self, creator_user_uid=None, active=True, name=None, hold_ext_ref=None
    ):
        """Gets all existing Legal Hold Matters.

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
            "legalHolds",
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
            "legalHoldMembershipUid": legal_hold_membership_uid,
            "legalHoldUid": legal_hold_uid,
            "userUid": user_uid,
            "user": user,
            "activeState": active_state,
            "pgNum": page_num,
            "pgSize": page_size,
        }
        uri = "/api/v1/LegalHoldMembership"
        try:
            return self._connection.get(uri, params=params)
        except Py42BadRequestError as ex:
            if "At least one criteria must be specified" in ex.response.text:
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
            "legalHoldMemberships",
            legal_hold_uid=legal_hold_uid,
            user_uid=user_uid,
            user=user,
            active=active,
        )

    def get_events_page(
        self,
        legal_hold_uid=None,
        min_event_date=None,
        max_event_date=None,
        page_num=1,
        page_size=None,
    ):
        """Gets an individual page of Legal Hold events.


        Args:
            legal_hold_uid (str, optional): Find LegalHoldEvents for the Legal Hold
                Matter with this unique identifier. Defaults to None.
            min_event_date (str or int or float or datetime, optional): Find
                LegalHoldEvents whose eventDate is equal to or after this time.
                E.g. yyyy-MM-dd HH:MM:SS. Defaults to None.
            max_event_date (str or int or float or datetime, optional): Find
                LegalHoldEvents whose eventDate is equal to or before this time.
                E.g. yyyy-MM-dd HH:MM:SS. Defaults to None.
            page_num (int): The page number to request. Defaults to 1.
            page_size (int, optional): The size of the page.
                Defaults to `py42.settings.items_per_page`.

        Returns:
            :class:`py42.response.Py42Response`:
        """
        page_size = page_size or settings.items_per_page
        if min_event_date:
            min_event_date = parse_timestamp_to_milliseconds_precision(min_event_date)
        if max_event_date:
            max_event_date = parse_timestamp_to_milliseconds_precision(max_event_date)
        params = {
            "legalHoldUid": legal_hold_uid,
            "minEventDate": min_event_date,
            "maxEventDate": max_event_date,
            "pgNum": page_num,
            "pgSize": page_size,
        }
        uri = "/api/v1/LegalHoldEventReport"

        return self._connection.get(uri, params=params)

    def get_all_events(
        self, legal_hold_uid=None, min_event_date=None, max_event_date=None
    ):
        """Gets an individual page of Legal Hold events.

        Args:
            legal_hold_uid (str, optional): Find LegalHoldEvents for the Legal Hold Matter
                with this unique identifier. Defaults to None.
            min_event_date (str or int or float or datetime, optional): Find
                LegalHoldEvents whose eventDate is equal to or after this time.
                E.g. yyyy-MM-dd HH:MM:SS. Defaults to None.
            max_event_date (str or int or float or datetime, optional): Find
                LegalHoldEvents whose eventDate is equal to or before this time.
                E.g. yyyy-MM-dd HH:MM:SS. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of LegalHoldEvent objects.
        """
        return get_all_pages(
            self.get_events_page,
            "legalHoldEvents",
            legal_hold_uid=legal_hold_uid,
            min_event_date=min_event_date,
            max_event_date=max_event_date,
        )

    def add_to_matter(self, user_uid, legal_hold_uid):
        """Add a user (Custodian) to a Legal Hold Matter.

        Args:
            user_uid (str): The identifier of the user.
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v1/LegalHoldMembership"
        data = {"legalHoldUid": legal_hold_uid, "userUid": user_uid}
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as err:
            if "USER_ALREADY_IN_HOLD" in err.response.text:
                matter = self.get_matter_by_uid(legal_hold_uid)
                matter_id_and_name_text = (
                    f"legal hold matter id={legal_hold_uid}, name={matter['name']}"
                )
                raise Py42UserAlreadyAddedError(err, user_uid, matter_id_and_name_text)
            raise

    def remove_from_matter(self, legal_hold_membership_uid):
        """Remove a user (Custodian) from a Legal Hold Matter.

        Args:
            legal_hold_membership_uid (str): The identifier of the LegalHoldMembership
                representing the Custodian to Matter relationship.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v1/LegalHoldMembershipDeactivation"
        data = {"legalHoldMembershipUid": legal_hold_membership_uid}
        return self._connection.post(uri, json=data)

    def deactivate_matter(self, legal_hold_uid):
        """Deactivates and closes a Legal Hold Matter.

        Args:
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v4/legal-hold-deactivation/update"
        data = {"legalHoldUid": legal_hold_uid}
        return self._connection.post(uri, json=data)

    def reactivate_matter(self, legal_hold_uid):
        """Reactivates and re-opens a closed Matter.

        Args:
            legal_hold_uid (str): The identifier of the Legal Hold Matter.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/v1/LegalHoldReactivation/{legal_hold_uid}"
        return self._connection.put(uri)
