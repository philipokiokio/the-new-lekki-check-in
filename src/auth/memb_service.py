# Framework Imports
from datetime import date
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# application imports
from src.app.utils.db_utils import hash_password, verify_password
from src.app.utils.mailer_util import send_mail
from src.app.utils.token import auth_retrieve_token, auth_settings, auth_token
from src.auth import schemas
from src.auth.memb_repo import token_repo, memb_repo
from src.auth.models import RefreshToken, Member
from src.attendance.attendance_repo import attendance_repo
from src.auth.oauth import (
    create_access_token,
    create_refresh_token,
    credential_exception,
)


def is_sunday() -> bool:
    day_ = date.today().isoweekday()
    if day_ != 7:
        return False

    return True


class MembService:
    def __init__(self):
        # Initializing Repositories
        self.memb_repo = memb_repo
        self.token_repo = token_repo
        self.attendance = attendance_repo

    def orm_call(self, memb: Member):
        memb_ = memb.__dict__
        if memb.is_admin:
            memb_["role"] = "Admin"
        elif memb.is_visitor:
            memb_["role"] = "Visitor"

        else:
            memb_["role"] = "Member"
        return memb_

    def create_attendance(self, member: Member):
        today = date.today().strftime("%Y-%m-%d")

        attendance_repo.create(
            {
                "member_id": member.id,
                "date": today,
                "year": date.today().year,
                "sunday_service": is_sunday(),
                "midweek_service": not is_sunday(),
            }
        )

    def check_in(self, member_mail: schemas.TokenData):
        memb_check = self.memb_repo.get_member(member_mail.email)
        church = "The New Lekki"
        if not memb_check:
            raise HTTPException(
                detail=f"you are not of member of {church}",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        memb_check: Member
        memb_check.attendance_count = memb_check.attendance_count + 1

        if memb_check.is_visitor:
            if memb_check.visitor_count == 4:
                memb_check.is_visitor = False
                # post req to THeNew DB

            else:
                memb_check.visitor_count = memb_check.visitor_count + 1

        memb_check = self.memb_repo.update(memb_check)
        self.create_attendance(memb_check)

        return {
            "message": "Successfully checked in for this service",
            "data": self.orm_call(memb_check),
            "status": status.HTTP_200_OK,
        }

    def join(self, member: schemas.Join):
        memb_check = self.memb_repo.get_member(member.email)
        if memb_check:
            raise HTTPException(
                detail="this is a member", status_code=status.HTTP_409_CONFLICT
            )
        phone_check = self.memb_repo.check_phone(member.phone_number)

        if phone_check:
            raise HTTPException(
                detail="This phone number belongs to another user",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        member_dict = member.dict()
        if member.is_visitor:
            member_dict["visitor_count"] = 1

        member_dict["attendance_count"] = 1
        member_dict["is_admin"] = False

        member = self.memb_repo.create(member_dict)
        self.create_attendance(member)

        church = "The New Lekki"
        return {
            "message": f"Vistor has joined {church}",
            "data": self.orm_call(member),
            "status": status.HTTP_201_CREATED,
        }

    async def register_admin(self, memb: schemas.AdminCreate) -> dict:
        # checking if user exists.
        memb_check = self.memb_repo.get_member(memb.email)

        # raise an Exception if user exists.
        if memb_check:
            if memb_check.is_admin:
                return self.orm_call(memb_check)
            # set_password
            memb_check.password = hash_password(memb.password)
            memb_check.is_admin = True
            self.memb_repo.update(memb_check)
            return self.orm_call(memb_check)

        # password hashing
        memb.password = hash_password(memb.password)

        # creating new user
        memb_dict = memb.dict()
        new_memb = self.memb_repo.create(memb_dict)
        # # create new access token
        # token = auth_token(new_user.email)

        # mail data inserted in to the  template
        # mail_data = {
        #     "first_name": new_user.name,
        #     "url": f"{auth_settings.frontend_url}/auth/verification/{token}/",
        # }
        # # mail title
        # mail_title = "Verify your Account"
        # template_pointer = "user/verification.html"
        # # send mail
        # await send_mail([new_user.email], mail_title, mail_data, template_pointer)

        return self.orm_call(new_memb)

    def login(self, member: OAuth2PasswordRequestForm) -> schemas.MessageLoginResponse:
        # check if user exists.
        memb_check = self.memb_repo.get_member(member.username)
        # raise exception if there is no user
        if not memb_check:
            raise HTTPException(
                detail="User does not exist", status_code=status.HTTP_400_BAD_REQUEST
            )

        # verify that the password is correct.
        pass_hash_check = verify_password(memb_check.password, member.password)
        # raise credential error
        if not pass_hash_check:
            credential_exception()
        # if user is not admin raise exception
        if memb_check.is_admin is False:
            raise HTTPException(
                detail="User Account is not verified",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        # create Access and Refresh Token
        memb_check_ = {"email": memb_check.email}
        access_token = create_access_token(memb_check_)
        refresh_token = create_refresh_token(memb_check_)
        # check if there is a previously existing refresh token
        token_check = self.token_repo.get_token(memb_check.id)
        # if token update token column
        if token_check:
            token_check.token = refresh_token
            self.token_repo.update_token(token_check)
        else:
            # create new token data
            self.token_repo.create_token(refresh_token, memb_check.id)

        # validating data via the DTO
        refresh_token_ = {"token": refresh_token, "header": "Refresh-Tok"}

        # DTO response
        resp = {
            "message": "Login Successful",
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token_,
            "status": status.HTTP_200_OK,
        }
        return resp

    def update_memb(self, update_member: schemas.MemberUpdate, memb: Member) -> dict:
        # update user
        update_memb_dict = update_member.dict(exclude_unset=True)

        for key, value in update_memb_dict.items():
            setattr(memb, key, value)

        return self.orm_call(self.memb_repo.update(memb))

    def update_memb_by_id(
        self, update_member: schemas.MemberUpdate, memb_id: int
    ) -> dict:
        # update user

        memb = self.memb_repo.get_by_id(memb_id)
        update_memb_dict = update_member.dict(exclude_unset=True)

        for key, value in update_memb_dict.items():
            setattr(memb, key, value)

        return self.orm_call(self.memb_repo.update(memb))

    def delete(self, memb: Member):
        # delete user
        return self.memb_repo.delete(memb)

    async def password_reset(self, memb_email: schemas.EmailStr):
        # check if user exist.
        memb = self.memb_repo.get_member(memb_email)
        # raise Exception if memb does not exist.
        if not memb:
            raise HTTPException(
                detail="memb does not exist", status_code=status.HTTP_404_NOT_FOUND
            )
        # create Timed Token
        token = auth_token(memb.email)
        # mail data
        mail_data = {
            "first_name": memb.name,
            "url": f"{auth_settings.frontend_url}/auth/verification/{token}/",
        }
        # mail subject
        mail_title = "Reset your Password"
        template_pointer = "/memb/verification.html"
        # send mail
        mail_status = await send_mail(
            [memb.email], mail_title, mail_data, template_pointer
        )
        # response based on the success or failure of sending mail
        if mail_status:
            return {
                "message": "Reset Mail sent successfully",
                "status": status.HTTP_200_OK,
                "mail_status": mail_status,
            }
        else:
            return {
                "message": "Reset Mail was not sent",
                "status": status.HTTP_400_BAD_REQUEST,
                "mail_status": mail_status,
            }

    def password_reset_complete(self, token: str, password_data: schemas.PasswordData):
        # extract data from timed token
        data = auth_retrieve_token(token)
        # if data is None raise Exception
        if data is None:
            raise HTTPException(
                detail="Token has expired.", status_code=status.HTTP_409_CONFLICT
            )
        # check for memb based on tokjen data

        memb = self.memb_repo.get_member(data)
        # raise exception if memb does not exist.
        if not memb:
            raise HTTPException(
                detail="memb does not exist", status_code=status.HTTP_404_NOT_FOUND
            )
        # update newly set password in hash
        memb.password = hash_password(password_data.password)
        # update memb
        self.memb_repo.update(memb)
        return {
            "message": "memb password set successfully",
            "status": status.HTTP_200_OK,
        }

    def change_password(self, memb: Member, password_data: schemas.ChangePassword):
        # verify oldpassword is saved in the DB
        password_check = verify_password(memb.password, password_data.old_password)
        # if not True raise Exception
        if not password_check:
            raise HTTPException(
                detail="Old Password does not corelate.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # hash new password
        memb.password = hash_password(password_data.password)
        # update memb
        memb = self.memb_repo.update(memb)
        # return memb
        return {
            "message": "Password changed successfully",
            "data": self.orm_call(memb),
            "status": status.HTTP_200_OK,
        }


# Instanting the UserService class
memb_service = MembService()
