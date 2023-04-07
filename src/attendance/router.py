from fastapi import APIRouter, status, Depends
from typing import Optional
from src.auth.oauth import get_current_user
from src.attendance.attendance_service import attendance_service
from datetime import date
from src.attendance.schemas import MessageListUserResp, MessageUserResp


admin_action_router = APIRouter(prefix="/api/v1/attendance", tags=["Admin Attendance"])


@admin_action_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=MessageListUserResp
)
def get_all_members(
    search_name: Optional[str] = None,
    is_sunday: Optional[bool] = None,
    is_midweek: Optional[bool] = None,
    date: Optional[date] = None,
    current_user: dict = Depends(get_current_user),
):
    return attendance_service.get_all_members(search_name, is_sunday, is_midweek, date)


@admin_action_router.get(
    "/member/{member_id}/",
    status_code=status.HTTP_200_OK,
    response_model=MessageUserResp,
)
def get_member(
    member_id: int,
    date: Optional[date] = None,
    is_sunday: Optional[bool] = None,
    is_midweek: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
):
    return attendance_service.get_user_attendance(
        date, member_id, is_sunday, is_midweek
    )


@admin_action_router.post(
    "/check-in/", status_code=status.HTTP_200_OK, response_model=MessageUserResp
)
def admin_member_check_in(
    search_name: Optional[str],
    search_email: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    return attendance_service.admin_check_in(search_name, search_email)
