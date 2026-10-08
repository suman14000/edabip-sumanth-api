from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ReportType = Literal["Scheduled", "On Demand"]
ReportStatus = Literal["Completed", "Failed", "Scheduled"]


class ReportBase(BaseModel):
    report_name: str = Field(..., min_length=1, max_length=200)
    module: str = Field(..., min_length=1, max_length=100)
    report_type: ReportType
    last_run: datetime | None = None
    owner: str = Field(..., min_length=1, max_length=100)
    status: ReportStatus = "Scheduled"
    run_time_seconds: float = Field(default=0, ge=0)
    template_id: int | None = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    report_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    module: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    report_type: ReportType | None = None
    last_run: datetime | None = None
    owner: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    status: ReportStatus | None = None
    run_time_seconds: float | None = Field(
        default=None,
        ge=0
    )
    template_id: int | None = None


class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportSummary(BaseModel):
    total_reports: int
    completed_reports: int
    failed_reports: int
    scheduled_reports: int
    average_run_time: float


class DistributionItem(BaseModel):
    name: str
    count: int