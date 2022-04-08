from py42.exceptions import Py42Error
from py42.services import BaseService
from py42.services.util import get_all_pages


class UserRiskProfileService(BaseService):

    _uri_prefix = "/v1/user-risk-profiles"

    def get(self, user_id):
        uri = f"{self._uri_prefix}/{user_id}"
        return self._connection.get(uri)

    def update(self, user_id, start_date=None, end_date=None, notes=None, paths=None):
        start_day, start_month, start_year = _parse_date_string(start_date)
        end_day, end_month, end_year = _parse_date_string(end_date)

        # if paths unspecified, assume provided values
        if not paths:
            paths = []
            if start_date:
                paths += "startDate"
            if end_date:
                paths += "endDate"
            if notes:
                paths += "notes"
        if not paths:
            raise Py42Error("No fields or paths provided. No values will be updated.")

        params = {"paths": ", ".join(paths)}
        data = {
            "endDate": {"day": end_day, "month": end_month, "year": end_year},
            "notes": notes,
            "startDate": {"day": start_day, "month": start_month, "year": start_year},
        }
        uri = f"{self._uri_prefix}/{user_id}"
        return self._connection.patch(uri, json=data, params=params)
        # Backend handles invalid dates

    def get_page(
        self,
        page=None,
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
            "page": page,
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
        data = {"cloudAliases": cloud_aliases, "userId": user_id}
        uri = f"{self._uri_prefix}/{user_id}/add-cloud-aliases"
        return self._connection.post(uri, json=data)

    def delete_cloud_aliases(self, user_id, cloud_aliases):
        if not isinstance(cloud_aliases, (list, tuple)):
            cloud_aliases = [cloud_aliases]
        data = {"cloudAliases": cloud_aliases, "userId": user_id}
        uri = f"{self._uri_prefix}/{user_id}/delete-cloud-aliases"
        return self._connection.post(uri, json=data)


def _parse_date_string(date):
    # assumes dates are in the format "DAY-MONTH-YEAR" (TODO - this can change)
    try:
        year, month, day = (int(i) for i in date.split("-"))
        return day, month, year
    except ValueError:
        raise Py42Error("Unable to parse date.  Expected format 'yyyy-mm-dd'.")
