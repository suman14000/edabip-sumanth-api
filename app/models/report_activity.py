from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReportActivity(Base):
    __tablename__ = "report_activity"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id"),
        nullable=False
    )

    activity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    activity_status: Mapped[str] = mapped_column(
        Enum("Success", "Failed", "Started"),
        nullable=False
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    execution_time_seconds: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0
    )

    executed_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    report = relationship(
        "Report",
        back_populates="activities"
    )