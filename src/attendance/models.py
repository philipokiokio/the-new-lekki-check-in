from src.app.utils.models_utils import AbstractModel
from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship


class Attendance(AbstractModel):
    __tablename__ = "attendance"
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    sunday_service = Column(Boolean, nullable=False)
    midweek_service = Column(Boolean, nullable=False)
    member = relationship("Member", passive_deletes=True)
