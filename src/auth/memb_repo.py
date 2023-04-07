# Pydantic imports
from pydantic import EmailStr

# application import
from src.app.utils.base_repository import BaseRepo
from src.auth.models import RefreshToken, Member
from typing import Optional
from datetime import date
from sqlalchemy import and_


class MemberRepo(BaseRepo):
    @property
    def base_query(self):
        # Base Query for DB calls
        return self.db.query(Member)

    def get_member(self, email: EmailStr) -> Optional[Member]:
        # get Member by email

        return self.base_query.filter(Member.email == email).first()

    def get_by_id(self, member_id: int) -> Optional[Member]:
        # get Member by email

        return self.base_query.filter(Member.id == member_id).first()

    def get_by_member_info(
        self, email: Optional[str], name: Optional[str]
    ) -> Optional[Member]:
        # get Member by email
        email_filter = []
        name_filter = []
        if email:
            email_filter.append(Member.email.ilike(f"%{email}%"))

        if name:
            name_filter.append(Member.name.ilike(f"%{name}%"))

        filters_ = name_filter + email_filter

        return self.base_query.filter(*filters_).first()

    def all_members(
        self,
        search: Optional[str],
        is_sunday: Optional[bool],
        is_midweek: Optional[bool],
        date_: Optional[date],
    ):
        name_filter = []
        sunday_filter = []
        midweek_filter = []
        date_filter = []

        if search:
            name_filter.append(Member.name.ilike(f"%{search}%"))
        if type(is_sunday) == bool:
            sunday_filter.append(Member.attendance.any(sunday_service=is_sunday))

        if type(is_midweek) == bool:
            midweek_filter.append(Member.attendance.any(midweek_service=is_midweek))

        if date_:
            date_filter.append(Member.attendance.any(date=date_))

        attendance_filter = sunday_filter + midweek_filter + date_filter + name_filter

        return self.base_query.filter(and_(*attendance_filter)).all()

    def create(self, member_create: dict) -> Member:
        # create a new Member
        new_Member = Member(**member_create)
        self.db.add(new_Member)
        self.db.commit()
        self.db.refresh(new_Member)
        return new_Member

    def delete(self, Member: Member):
        # delete Member

        self.db.delete(Member)
        self.db.commit()

    def update(self, Member: Member):
        # update Member
        updated_Member = Member
        self.db.commit()
        self.db.refresh(updated_Member)
        return updated_Member


class TokenRepo(BaseRepo):
    def base_query(self):
        # base query for refresh token
        return self.db.query(RefreshToken)

    def create_token(self, refresh_token: str, member_id: int) -> RefreshToken:
        # store refresh token
        refresh_token = RefreshToken(token=refresh_token, member_id=member_id)
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    def get_token(self, member_id: int):
        # filter by Member_id
        return self.base_query().filter(RefreshToken.member_id == member_id).first()

    def get_token_by_tok(self, token: str):
        # filter by token
        return self.base_query().filter(RefreshToken.token == token).first()

    def update_token(self, update_token) -> RefreshToken:
        # update token
        self.db.commit()
        self.db.refresh(update_token)
        return update_token


# Instatiating the Classes.

memb_repo = MemberRepo()
token_repo = TokenRepo()
