# python imports
from datetime import datetime
from typing import Optional

# 3rd party
from pydantic import EmailStr, constr

# application import
from src.app.utils.schemas_utils import AbstractModel, ResponseModel


# Member DTO
class Join(AbstractModel):
    name: str
    email: EmailStr
    phone_number: constr(min_length=11, max_length=11)
    is_visitor: bool


# Email DTO (Used for token verification)
class TokenData(AbstractModel):
    email: EmailStr


# Create new user
class AdminCreate(AbstractModel):
    name: str
    email: EmailStr
    password: str
    is_admin: bool = True


# ORM response
class MemberResponse(AbstractModel):
    name: str
    email: EmailStr
    role: str
    date_created: datetime


# Password Data for password reset
class PasswordData(AbstractModel):
    password: str


# Password data for Change Password
class ChangePassword(PasswordData):
    old_password: str


# User Update DTO
class MemberUpdate(AbstractModel):
    name: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]


# Req-Res Response DTO
class MessageMembResponse(ResponseModel):
    data: MemberResponse


# Token DTO
class Token(AbstractModel):
    token: str


# Refresh Token DTO
class RefreshToken(Token):
    header: str


# Req-Res Login Response
class MessageLoginResponse(ResponseModel):
    access_token: str
    token_type: str
    refresh_token: RefreshToken
