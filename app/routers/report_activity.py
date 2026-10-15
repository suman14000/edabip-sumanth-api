import csv
from datetime import datetime
from io import StringIO
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.report_activity import ReportActivity
from app.models.report import Report
from app.models.user import User
from app.repositories.activity_repository import list_activities
from app.schemas.report_activity import (
    ReportActivityCreate,
    ReportActivityResponse,
)

router = APIRouter(
    prefix="/api/report-activity",
    tags=["Report Activity"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[ReportActivityResponse])
def read_activities(
    report_id: int | None = Query(default=None, gt=0),
    activity_status: Literal["Success", "Failed", "Started"] | None = None,
    search: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=422,
            detail="date_from must be earlier than or equal to date_to",
        )

    return list_activities(
        db=db,
        report_id=report_id,
        activity_status=activity_status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        skip=(page - 1) * limit,
        limit=limit,
    )


@router.get("/export/csv")
def export_activity_csv(
    report_id: int | None = Query(default=None, gt=0),
    activity_status: Literal["Success", "Failed", "Started"] | None = None,
    search: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    db: Session = Depends(get_db),
):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=422,
            detail="date_from must be earlier than or equal to date_to",
        )

    # Export the full matching activity set, not just the first page.
    activities = list_activities(
        db=db,
        report_id=report_id,
        activity_status=activity_status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        skip=0,
        limit=100000,
    )

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "id",
        "report_id",
        "activity_type",
        "activity_status",
        "message",
        "execution_time_seconds",
        "executed_by",
        "created_at",
    ])

    for item in activities:
        writer.writerow([
            item.id,
            item.report_id,
            item.activity_type,
            item.activity_status,
            item.message or "",
            item.execution_time_seconds,
            item.executed_by or "",
            item.created_at.isoformat() if item.created_at else "",
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="recent_activity.csv"'
        },
    )


@router.post(
    "",
    response_model=ReportActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    payload: ReportActivityCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    report = db.query(Report).filter(
        Report.id == payload.report_id
    ).first()

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    activity = ReportActivity(**payload.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


@router.get("/{activity_id}", response_model=ReportActivityResponse)
def read_activity(
    activity_id: int,
    db: Session = Depends(get_db),
):
    activity = db.query(ReportActivity).filter(
        ReportActivity.id == activity_id
    ).first()

    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    return activity


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    activity = db.query(ReportActivity).filter(
        ReportActivity.id == activity_id
    ).first()

    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    db.delete(activity)
    db.commit()

    return {"message": "Activity deleted", "activity_id": activity_id}