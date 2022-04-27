import datetime

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CloudAliasCharacterLimitExceededError
from py42.exceptions import Py42CloudAliasLimitExceededError
from py42.exceptions import Py42Error
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserRiskProfileNotFound
from py42.services import BaseService
from py42.services.util import get_all_pages

_DATE_FORMAT = "%Y-%m-%d"


class UserRiskProfileService(BaseService):

    _uri_prefix = "/v1/user-risk-profiles"

    def get_by_id(self, user_id):
        uri = f"{self._uri_prefix}/{user_id}"
        try:
            return self._connection.get(uri)
        # catch not found error
        except Py42NotFoundError as err:
            raise Py42UserRiskProfileNotFound(err, user_id)

    def get_by_username(self, username):
        user_id = None
        generator = self.get_all()

        # get the first page of user profiles
        for page in generator:
            for user in page.data["userRiskProfiles"]:
                if user["username"] == username:
                    user_id = user["userId"]
                    break

        try:
            return self.get_by_id(user_id)
        except Py42NotFoundError as err:
            raise Py42UserRiskProfileNotFound(err, username, identifier="username")

    def update(self, user_id, start_date=None, end_date=None, notes=None):
        # Build paths field
        paths = []
        data = {}
        if start_date is not None:
            paths += ["startDate"]
            if start_date == "":
                data["startDate"] = None
            else:
                start_day, start_month, start_year = _parse_date_string(start_date)
                data["startDate"] = {
                    "day": start_day,
                    "month": start_month,
                    "year": start_year,
                }
        if end_date is not None:
            paths += ["endDate"]
            if end_date == "":
                data["endDate"] = None
            else:
                end_day, end_month, end_year = _parse_date_string(end_date)
                data["endDate"] = {"day": end_day, "month": end_month, "year": end_year}
        if notes is not None:
            paths += ["notes"]
            if notes == "":
                data["notes"] = None
            else:
                data["notes"] = notes
        if not paths:
            raise Py42Error("No fields provided. No values will be updated.")

        params = {"paths": ", ".join(paths)}
        uri = f"{self._uri_prefix}/{user_id}"
        try:
            return self._connection.patch(uri, json=data, params=params)
        # catch not found error
        except Py42NotFoundError as err:
            raise Py42UserRiskProfileNotFound(err, user_id)
        # Backend handles invalid dates

    def get_page(
        self,
        page_num=None,
        page_size=None,
        manager_id=None,
        title=None,
        division=None,
        department=None,
        employment_type=None,
        country=None,
        region=None,
        locality=None,
        active=None,
        deleted=None,
        support_user=None,
    ):
        data = {
            "page": page_num,
            "page_size": page_size,
            "manager_id": manager_id,
            "title": title,
            "division": division,
            "department": department,
            "employment_type": employment_type,
            "country": country,
            "region": region,
            "locality": locality,
            "active": active,
            "deleted": deleted,
            "support_user": support_user,
        }
        return self._connection.get(self._uri_prefix, params=data)

    def get_all(
        self,
        manager_id=None,
        title=None,
        division=None,
        department=None,
        employment_type=None,
        country=None,
        region=None,
        locality=None,
        active=None,
        deleted=None,
        support_user=None,
    ):
        return get_all_pages(
            self.get_page,
            "userRiskProfiles",
            manager_id=manager_id,
            title=title,
            division=division,
            department=department,
            employment_type=employment_type,
            country=country,
            region=region,
            locality=locality,
            active=active,
            deleted=deleted,
            support_user=support_user,
        )

    def add_cloud_aliases(self, user_id, cloud_aliases):
        if not isinstance(cloud_aliases, (list, tuple)):
            cloud_aliases = [cloud_aliases]

        # frontend limits aliases to 50 characters
        for alias in cloud_aliases:
            if len(alias) > 50:
                raise Py42CloudAliasCharacterLimitExceededError

        data = {"cloudAliases": cloud_aliases, "userId": user_id}
        uri = f"{self._uri_prefix}/{user_id}/add-cloud-aliases"

        try:
            return self._connection.post(uri, json=data)
        # catch not found error
        except Py42NotFoundError as err:
            raise Py42UserRiskProfileNotFound(err, user_id)
        # catch cloud username limit exceeded
        except Py42BadRequestError as err:
            if "Cloud usernames must be less than or equal to" in err.response.text:
                raise Py42CloudAliasLimitExceededError(err)
            raise

    def delete_cloud_aliases(self, user_id, cloud_aliases):
        if not isinstance(cloud_aliases, (list, tuple)):
            cloud_aliases = [cloud_aliases]
        data = {"cloudAliases": cloud_aliases, "userId": user_id}
        uri = f"{self._uri_prefix}/{user_id}/delete-cloud-aliases"
        try:
            return self._connection.post(uri, json=data)
        # catch not found error
        except Py42NotFoundError as err:
            raise Py42UserRiskProfileNotFound(err, user_id)


def _parse_date_string(date):
    # handle date-time
    if isinstance(date, (datetime.date, datetime.datetime)):
        date = date.strftime(_DATE_FORMAT)

    # assumes dates are in the format "yyyy-mm-dd"
    try:
        year, month, day = (int(i) for i in date.split("-"))
        return day, month, year
    except ValueError:
        raise Py42Error("Unable to parse date.  Expected format 'yyyy-mm-dd'.")
