from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report import Report
from app.models.report_activity import ReportActivity
from app.schemas.report_activity import (
    ReportActivityCreate,
    ReportActivityResponse,
)


router = APIRouter(
    prefix="/api/report-activity",
    tags=["Report Activity"]
)


@router.post(
    "",
    response_model=ReportActivityResponse,
    status_code=201
)
def create_activity(
    activity_data: ReportActivityCreate,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(
            Report.id == activity_data.report_id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    activity = ReportActivity(
        report_id=activity_data.report_id,
        activity_type=activity_data.activity_type,
        activity_status=activity_data.activity_status,
        message=activity_data.message,
        execution_time_seconds=(
            activity_data.execution_time_seconds
        ),
        executed_by=activity_data.executed_by,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


@router.get(
    "",
    response_model=list[ReportActivityResponse]
)
def get_activities(
    report_id: int | None = Query(default=None),
    activity_status: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(ReportActivity)

    if report_id is not None:
        query = query.filter(
            ReportActivity.report_id == report_id
        )

    if activity_status:
        if activity_status not in [
            "Success",
            "Failed",
            "Started"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Invalid activity status"
            )

        query = query.filter(
            ReportActivity.activity_status
            == activity_status
        )

    return (
        query
        .order_by(ReportActivity.id.desc())
        .all()
    )


@router.get(
    "/{activity_id}",
    response_model=ReportActivityResponse
)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = (
        db.query(ReportActivity)
        .filter(
            ReportActivity.id == activity_id
        )
        .first()
    )

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Report activity not found"
        )

    return activity


@router.delete(
    "/{activity_id}"
)
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    activity = (
        db.query(ReportActivity)
        .filter(
            ReportActivity.id == activity_id
        )
        .first()
    )

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Report activity not found"
        )

    db.delete(activity)
    db.commit()

    return {
        "message": "Report activity deleted successfully",
        "activity_id": activity_id
    }