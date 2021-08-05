from py42 import settings
from py42.services import BaseService
from py42.services.util import get_all_pages
from py42.util import parse_timestamp_to_microseconds_precision
from py42.util import to_list

_FILTER_PARAMS = (
    "event_types",
    "user_ids",
    "usernames",
    "user_ip_addresses",
    "affected_user_ids",
    "affected_usernames",
    "begin_time",
    "end_time",
)

HEADER_MAP = {"CSV": {"Accept": "text/csv"}, "CEF": {"Accept": "text/x-cef"}}


class AuditLogsService(BaseService):
    """https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Search_Audit_Log_events_with_the_Code42_API"""

    def get_page(
        self,
        page_num=1,
        page_size=None,
        begin_time=None,
        end_time=None,
        event_types=None,
        user_ids=None,
        usernames=None,
        user_ip_addresses=None,
        affected_user_ids=None,
        affected_usernames=None,
        format=None,
        **kwargs
    ):
        date_range = {}
        if begin_time:
            date_range["startTime"] = parse_timestamp_to_microseconds_precision(
                begin_time
            )
        if end_time:
            date_range["endTime"] = parse_timestamp_to_microseconds_precision(end_time)

        uri = "/rpc/search/search-audit-log"
        page_size = page_size or settings.items_per_page
        params = dict(
            page=page_num - 1,
            pageSize=page_size,
            dateRange=date_range,
            eventTypes=to_list(event_types),
            actorIds=to_list(user_ids),
            actorNames=to_list(usernames),
            actorIpAddresses=to_list(user_ip_addresses),
            affectedUserIds=to_list(affected_user_ids),
            affectedUserNames=to_list(affected_usernames),
        )
        params.update(**kwargs)

        headers = HEADER_MAP.get(format.upper()) if format else None
        return self._connection.post(uri, json=params, headers=headers)

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
        **kwargs
    ):
        return get_all_pages(
            self.get_page,
            "events",
            begin_time=begin_time,
            end_time=end_time,
            event_types=event_types,
            user_ids=user_ids,
            usernames=usernames,
            user_ip_addresses=user_ip_addresses,
            affected_user_ids=affected_user_ids,
            affected_usernames=affected_usernames,
            **kwargs
        )
