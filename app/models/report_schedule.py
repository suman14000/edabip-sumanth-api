from sqlalchemy import String, DateTime, Boolean, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), nullable=False, index=True)
    frequency: Mapped[str] = mapped_column(Enum("Daily", "Weekly", "Monthly", name="schedule_frequency_enum"), nullable=False)
    next_run: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
