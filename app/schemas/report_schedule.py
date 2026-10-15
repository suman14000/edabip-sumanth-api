from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Frequency = Literal["Daily", "Weekly", "Monthly"]


class ScheduleCreate(BaseModel):
    report_id: int = Field(gt=0)
    frequency: Frequency
    next_run: datetime
    active: bool = True


class ScheduleUpdate(BaseModel):
    frequency: Frequency | None = None
    next_run: datetime | None = None
    active: bool | None = None


class ScheduleResponse(BaseModel):
    id: int
    report_id: int
    frequency: Frequency
    next_run: datetime
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)