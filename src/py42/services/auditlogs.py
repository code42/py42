from py42 import settings
from py42.services import BaseService
from py42.services.util import get_all_pages
from py42.util import convert_datetime_to_timestamp_str
from py42.util import to_list


class AuditLogsService(BaseService):
    def get_page(self, page_num, page_size=None, **kwargs):

        uri = u"/rpc/search/search-audit-log"
        page_size = page_size or settings.items_per_page
        params = dict(
            page=page_num - 1,
            pageSize=page_size,
            dateRange=kwargs["date_range"],
            eventTypes=kwargs["event_types"],
            actorIds=kwargs["user_ids"],
            actorNames=kwargs["usernames"],
            actorIpAddresses=kwargs["user_ip_addresses"],
            affectedUserIds=kwargs["affected_user_ids"],
            affectedUserNames=kwargs["affected_usernames"],
        )
        params["type$"] = "audit_log::audit_log_queries.search_audit_log/1"
        return self._connection.post(uri, json=params)

    def get_all(
        self,
        begin_time=None,
        end_time=None,
        event_types=None,
        user_ids=None,
        usernames=None,
        user_ip_addresses=None,
        affected_user_ids=None,
        affected_usernames=None,
    ):

        event_types = to_list(event_types)
        user_ids = to_list(user_ids)
        usernames = to_list(usernames)
        user_ip_addresses = to_list(user_ip_addresses)
        affected_user_ids = to_list(affected_user_ids)
        affected_usernames = to_list(affected_usernames)

        date_range = {}
        if begin_time:
            date_range["startTime"] = convert_datetime_to_timestamp_str(begin_time)
        if end_time:
            date_range["endTime"] = convert_datetime_to_timestamp_str(end_time)

        return get_all_pages(
            self.get_page,
            "events",
            date_range=date_range,
            event_types=event_types,
            user_ids=user_ids,
            usernames=usernames,
            user_ip_addresses=user_ip_addresses,
            affected_user_ids=affected_user_ids,
            affected_usernames=affected_usernames,
        )
