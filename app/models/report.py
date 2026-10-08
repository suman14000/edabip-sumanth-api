from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    report_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    report_type: Mapped[str] = mapped_column(
        Enum("Scheduled", "On Demand"),
        nullable=False
    )

    last_run: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    owner: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        Enum("Completed", "Failed", "Scheduled"),
        nullable=False,
        default="Scheduled"
    )

    run_time_seconds: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0
    )

    template_id: Mapped[int | None] = mapped_column(
        ForeignKey("report_templates.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    template = relationship(
        "ReportTemplate",
        back_populates="reports"
    )

    activities = relationship(
        "ReportActivity",
        back_populates="report",
        cascade="all, delete-orphan"
    )