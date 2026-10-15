from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.report import Report
from app.models.report_template import ReportTemplate
from app.models.user import User
from app.repositories.report_repository import (
    create_report,
    delete_report,
    get_report,
    list_reports,
    update_report,
)
from app.schemas.report import (
    DistributionItem,
    ReportCreate,
    ReportResponse,
    ReportSummary,
    ReportUpdate,
)
from app.services.report_service import (
    get_report_status_distribution,
    get_report_summary,
    get_report_type_distribution,
)

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/summary", response_model=ReportSummary)
def summary(db: Session = Depends(get_db)):
    return get_report_summary(db)


@router.get("/type-distribution", response_model=list[DistributionItem])
def type_distribution(db: Session = Depends(get_db)):
    return get_report_type_distribution(db)


@router.get("/status-distribution", response_model=list[DistributionItem])
def status_distribution(db: Session = Depends(get_db)):
    return get_report_status_distribution(db)


@router.get("", response_model=list[ReportResponse])
def read_reports(
    search: str | None = None,
    module: str | None = None,
    report_type: Literal["Scheduled", "On Demand"] | None = None,
    report_status: Literal["Completed", "Failed", "Scheduled"] | None = Query(
        default=None, alias="status"
    ),
    owner: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort_by: Literal[
        "id", "report_name", "module", "report_type",
        "status", "owner", "created_at", "last_run"
    ] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=422,
            detail="date_from must be earlier than or equal to date_to",
        )

    return list_reports(
        db=db,
        search=search,
        module=module,
        report_type=report_type,
        status=report_status,
        owner=owner,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        order=order,
        skip=(page - 1) * limit,
        limit=limit,
    )


@router.get("/{report_id}", response_model=ReportResponse)
def read_report(report_id: int, db: Session = Depends(get_db)):
    report = get_report(db, report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    values = payload.model_dump()

    if values["template_id"] is not None:
        template = db.query(ReportTemplate).filter(
            ReportTemplate.id == values["template_id"]
        ).first()

        if template is None:
            raise HTTPException(status_code=404, detail="Template not found")

    return create_report(db, values)


@router.put("/{report_id}", response_model=ReportResponse)
def edit_report(
    report_id: int,
    payload: ReportUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    report = get_report(db, report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    values = payload.model_dump(exclude_unset=True)

    if values.get("template_id") is not None:
        template = db.query(ReportTemplate).filter(
            ReportTemplate.id == values["template_id"]
        ).first()

        if template is None:
            raise HTTPException(status_code=404, detail="Template not found")

    return update_report(db, report, values)


@router.post("/{report_id}/rerun")
def rerun_report(
    report_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    report = get_report(db, report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    # This records a re-run request; a background execution engine is not
    # part of this assignment. Update status and timestamp for the demo.
    report.status = "Scheduled"
    db.commit()
    db.refresh(report)

    return {
        "message": "Report re-run requested",
        "report_id": report.id,
        "status": report.status,
    }


@router.delete("/{report_id}")
def remove_report(
    report_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    report = get_report(db, report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    delete_report(db, report)

    return {"message": "Report deleted", "report_id": report_id}