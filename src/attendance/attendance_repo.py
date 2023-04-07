from src.app.utils.base_repository import BaseRepo
from src.attendance.models import Attendance
from datetime import date
from typing import Optional


class AttendanceRepo(BaseRepo):
    @property
    def base_query(self):
        return self.db.query(Attendance)

    def create(self, attendance_data: dict):
        new_attendance = Attendance(**attendance_data)
        self.db.add(new_attendance)
        self.db.commit()
        self.db.refresh(new_attendance)
        return new_attendance

    def all(
        self,
        date_: Optional[date],
        user_id: Optional[int],
        is_sunday: Optional[bool],
        is_midweek: Optional[bool],
    ):
        date_filter = []
        if date_:
            date_filter.append(Attendance.date == date_)
        mid_week_arr = []
        if type(is_midweek) == bool:
            mid_week_arr.append(Attendance.midweek_service == is_midweek)
        sunday_arr = []
        if type(is_sunday) == bool:
            sunday_arr.append(Attendance.sunday_service == is_sunday)

        filter_arr = date_filter + mid_week_arr + sunday_arr
        return self.base_query.filter(
            Attendance.member_id == user_id, *filter_arr
        ).all()


attendance_repo = AttendanceRepo()
