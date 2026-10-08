from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReportTemplateBase(BaseModel):
    template_name: str = Field(
        ...,
        min_length=1,
        max_length=150
    )
    description: str | None = None
    module: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    created_by: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


class ReportTemplateCreate(ReportTemplateBase):
    pass


class ReportTemplateUpdate(BaseModel):
    template_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )
    description: str | None = None
    module: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    created_by: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )


class ReportTemplateResponse(ReportTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)