from src.app.utils.base_repository import BaseRepo
from src.attendance.models import Attendance


class AttendanceRepo(BaseRepo):
    def create(self, attendance_data: dict):
        new_attendance = Attendance(**attendance_data)
        self.db.add(new_attendance)
        self.db.commit()
        self.db.refresh(new_attendance)
        return new_attendance


attendance_repo = AttendanceRepo()
