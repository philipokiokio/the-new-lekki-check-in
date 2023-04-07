# 3rd party imports
from sqlalchemy import Boolean, Column, ForeignKey, String, text, Integer
from sqlalchemy.orm import relationship

# application imports
from src.app.utils.models_utils import AbstractModel


class Member(AbstractModel):
    # Member Table
    __tablename__ = "members"
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_visitor = Column(Boolean, nullable=False, server_default=text("false"))
    visitor_count = Column(Integer, nullable=False)
    attendance_count = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default=text("false"))
    attendance = relationship("Attendance", back_populates="member")


class RefreshToken(AbstractModel):
    # Refresh Token Table
    __tablename__ = "refresh_tokens"
    member_id = Column(ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    user = relationship("Member", passive_deletes=True)
