from src.attendance.models import Attendance
from src.auth.memb_repo import Member, memb_repo
from typing import Optional
from fastapi import HTTPException, status
from src.attendance.attendance_repo import attendance_repo
from datetime import date


class AttendanceService:
    def __init__(self) -> None:
        self.user = memb_repo
        self.attendance = attendance_repo

    def orm_call(self, member: Member):
        member_ = member.__dict__
        member_["attendance"] = member.attendance
        return member_

    def get_all_members(
        self,
        search: Optional[str],
        is_sunday: Optional[bool],
        is_midweek: Optional[bool],
        date_: Optional[date],
    ):
        users = self.user.all_members(search, is_sunday, is_midweek, date_)

        if not users:
            raise HTTPException(
                detail="No Members available", status_code=status.HTTP_400_BAD_REQUEST
            )

        members = []

        for user in users:
            members.append(self.orm_call(user))

        return {
            "message": "All members returned successfully",
            "data": members,
            "status": status.HTTP_200_OK,
        }

    def get_user_attendance(
        self,
        date: Optional[date],
        member_id: int,
        is_sunday: Optional[bool],
        is_midweek: Optional[bool],
    ):
        attendance = self.attendance.all(date, member_id, is_sunday, is_midweek)

        if attendance is None:
            raise HTTPException(
                detail="No Attendance for any member",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        user = self.user.get_by_id(member_id)

        member = user.__dict__
        member["attendance"] = attendance

        return {
            "message": "attendance retieved successfully",
            "data": member,
            "status": status.HTTP_200_OK,
        }

    def create_attendance(self, member: Member):
        today = date.today().strftime("%Y-%m-%d")

        attendance_repo.create(
            {
                "member_id": member.id,
                "date": today,
                "year": date.today().year,
                "sunday_service": self.is_sunday(),
                "midweek_service": not self.is_sunday(),
            }
        )

    def is_sunday(self) -> bool:
        day_ = date.today().isoweekday()
        if day_ != 7:
            return False

        return True

    def admin_check_in(self, search_name: Optional[str], search_email: Optional[str]):
        member = self.user.get_by_member_info(search_email, search_name)
        if member is None:
            raise HTTPException(
                detail="No member with this name or email at The New Lekki",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        member.attendance_count = member.attendance_count + 1

        if member.is_visitor:
            if member.visitor_count == 4:
                member.is_visitor = False

            else:
                member.visitor_count = member.visitor_count + 1
        member = self.user.update(member)
        self.create_attendance(member)

        member_ = member.__dict__
        member_["attendance"] = member.attendance
        return {
            "message": "member checked-in sucessfully",
            "data": member_,
            "status": status.HTTP_200_OK,
        }


attendance_service = AttendanceService()
