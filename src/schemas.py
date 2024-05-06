from enum import Enum
from typing import Annotated, List
from pydantic import AfterValidator, BaseModel

from validators import validate_iso_date


class GroupType(str, Enum):
    hour = "hour"
    day = "day"
    month = "month"


ISODate = Annotated[str, AfterValidator(validate_iso_date)]


class InputSchema(BaseModel):
    dt_from: ISODate
    dt_upto: ISODate
    group_type: GroupType


class OutputSchema(BaseModel):
    dataset: List[int]
    labels: List[str]
