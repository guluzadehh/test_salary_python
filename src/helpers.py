from datetime import datetime
from dateutil.relativedelta import relativedelta
from schemas import GroupType


def create_group_key(group_type: GroupType) -> object:
    output = {"year": {"$year": {"$toDate": "$dt"}}}
    output["month"] = {"$month": {"$toDate": "$dt"}}

    if group_type == GroupType.day or group_type == GroupType.hour:
        output["day"] = {"$dayOfMonth": {"$toDate": "$dt"}}

    if group_type == GroupType.hour:
        output["hour"] = {"$hour": {"$toDate": "$dt"}}

    return output


def increment_date(dt: datetime, group_type: GroupType) -> datetime:
    if group_type == GroupType.month:
        return dt + relativedelta(months=1)
    elif group_type == GroupType.day:
        return dt + relativedelta(days=1)
    elif group_type == GroupType.hour:
        return dt + relativedelta(hours=1)
