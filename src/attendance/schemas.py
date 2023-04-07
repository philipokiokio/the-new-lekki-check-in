from src.app.utils.schemas_utils import ResponseModel, AbstractModel
from pydantic import constr
from datetime import date
from typing import List


class Attendance(AbstractModel):
    date: date
    year: int
    sunday_service: bool
    midweek_service: bool


class UserAttendance(AbstractModel):
    id: int
    name: str
    email: str
    phone_number: constr(min_length=11, max_length=11)
    is_visitor: bool
    visitor_count: int
    attendance_count: int
    attendance: List[Attendance]


class MessageListUserResp(ResponseModel):
    data: List[UserAttendance]


class MessageUserResp(ResponseModel):
    data: UserAttendance
