from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Index,
)
from sqlalchemy.sql import func

from app.database import Base


class ReportSchedule(Base):
    __tablename__ = "report_schedules"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(
        Integer,
        ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    frequency = Column(
        Enum("Daily", "Weekly", "Monthly", name="schedule_frequency"),
        nullable=False,
    )

    next_run = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        Index("idx_schedule_active_next_run", "active", "next_run"),
    )