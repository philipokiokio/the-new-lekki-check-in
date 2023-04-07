# framework imports
from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# application imports
from src.auth import schemas
from src.auth.memb_service import memb_service
from src.auth.oauth import get_current_user, verify_refresh_token

# API Router
memb_router = APIRouter(prefix="/api/v1/auth", tags=["Member Authentication"])
fellowship_router = APIRouter(prefix="/api/v1/fellowship", tags=["Fellowship Check-in"])


@fellowship_router.post(
    "/check-in/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageMembResponse,
)
def check_in(check_in: schemas.TokenData):
    return memb_service.check_in(check_in)


@memb_router.post(
    "/admin-join/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageMembResponse,
)
def join(join: schemas.Join, current_user: dict = Depends(get_current_user)):
    return memb_service.join(join)


@memb_router.post(
    "/join/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageMembResponse,
)
def join(join: schemas.Join):
    return memb_service.join(join)


@memb_router.post(
    "/register-admin/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageMembResponse,
)
async def register(admin_create: schemas.AdminCreate):
    """Registration of User

    Args:
        user_create (schemas.user_create): {
        "first_name", "last_name","email", "password"
        }

    Returns:
        _type_: response
    """
    new_user = await memb_service.register_admin(admin_create)
    return {
        "message": "Registration Successful",
        "data": new_user,
        "status": status.HTTP_201_CREATED,
    }


@memb_router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageLoginResponse,
)
def login(login_user: OAuth2PasswordRequestForm = Depends()):
    """Login

    Args:
        login_user (OAuth2PasswordRequestForm, optional):username, password

    Returns:
        _type_: user
    """
    user_login = memb_service.login(login_user)
    return user_login


@memb_router.get(
    "/me/", status_code=status.HTTP_200_OK, response_model=schemas.MessageMembResponse
)
def logged_in_user(current_user: dict = Depends(get_current_user)):
    """ME

    Args:
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): User data.

    Returns:
        _type_: User
    """
    return {
        "message": "Me Data",
        "data": memb_service.orm_call(current_user),
        "status": status.HTTP_200_OK,
    }


@memb_router.patch(
    "/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageMembResponse,
)
def update_user(
    user_id: int,
    update_memb: schemas.MemberUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update User

    Args:
        update_user (schemas.UserUpdate): all user fields.
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User.

    Returns:
        _type_: resp
    """
    update_user = memb_service.update_memb(update_memb, current_user)

    return {
        "message": "User Updated Successfully",
        "data": update_user,
        "status": status.HTTP_200_OK,
    }


@memb_router.patch(
    "/update/{memb_id}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageMembResponse,
)
def update_member_by_id(
    memb_id: int,
    update_memb: schemas.MemberUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update User

    Args:
        update_user (schemas.UserUpdate): all user fields.
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User.

    Returns:
        _type_: resp
    """
    update_user = memb_service.update_memb_by_id(update_memb, memb_id)

    return {
        "message": "User Updated Successfully",
        "data": update_user,
        "status": status.HTTP_200_OK,
    }


@memb_router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: dict = Depends(get_current_user)):
    """Delete User

    Args:
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User

    Returns:
        _type_: 204
    """
    memb_service.delete(current_user)
    return {"status": status.HTTP_204_NO_CONTENT}


@memb_router.get("/refresh/", status_code=status.HTTP_200_OK)
def get_new_token(new_access_token: str = Depends(verify_refresh_token)):
    """New Access token

    Args:
        new_access_token (str, optional): _description_. Defaults to Depends(verify_refresh_token): Gets Access token based on refresh token.

    Returns:
        _type_: _description_
    """
    return {
        "message": "New access token created successfully",
        "token": new_access_token,
        "status": status.HTTP_200_OK,
    }


@memb_router.patch(
    "/change-password/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageMembResponse,
)
def change_password(
    password_data: schemas.ChangePassword,
    current_user: dict = Depends(get_current_user),
):
    """Change Password

    Args:
        password_data (schemas.ChangePassword): {password, old_password}
        current_user (dict, optional): _description_. Defaults to Depends(get_current_user): Logged In User

    Returns:
        _type_: response
    """
    resp = memb_service.change_password(current_user, password_data)
    return resp


@memb_router.post("/password-reset/complete/{token}/", status_code=status.HTTP_200_OK)
def password_reset_complete(token: str, password_data: schemas.PasswordData):
    """Password Reset

    Args:
        token (str): _description_: Password reset token
        password_data (schemas.PasswordData): {password}

    Returns:
        _type_: resp
    """
    resp = memb_service.password_reset_complete(token, password_data)
    return resp


@memb_router.post("/reset-password/", status_code=status.HTTP_200_OK)
async def reset_password(password_data: schemas.TokenData):
    """Reset Password

    Args:
        password_data (schemas.TokenData): eemail

    Returns:
        _type_: response
    """
    resp = await memb_service.password_reset(password_data.email)
    return resp
