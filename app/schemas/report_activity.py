from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ActivityStatus = Literal["Success", "Failed", "Started"]


class ReportActivityBase(BaseModel):
    report_id: int
    activity_type: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    activity_status: ActivityStatus
    message: str | None = None
    execution_time_seconds: float = Field(
        default=0,
        ge=0
    )
    executed_by: str | None = Field(
        default=None,
        max_length=100
    )


class ReportActivityCreate(ReportActivityBase):
    pass


class ReportActivityResponse(ReportActivityBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)