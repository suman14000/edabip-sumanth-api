from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report import Report
from app.models.report_template import ReportTemplate
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
    tags=["Reports"]
)


@router.get(
    "/summary",
    response_model=ReportSummary
)
def report_summary(
    db: Session = Depends(get_db)
):
    return get_report_summary(db)


@router.get(
    "/type-distribution",
    response_model=list[DistributionItem]
)
def report_type_distribution(
    db: Session = Depends(get_db)
):
    return get_report_type_distribution(db)


@router.get(
    "/status-distribution",
    response_model=list[DistributionItem]
)
def report_status_distribution(
    db: Session = Depends(get_db)
):
    return get_report_status_distribution(db)


@router.post(
    "",
    response_model=ReportResponse,
    status_code=201
)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db)
):
    if report_data.template_id is not None:
        template = (
            db.query(ReportTemplate)
            .filter(
                ReportTemplate.id == report_data.template_id
            )
            .first()
        )

        if not template:
            raise HTTPException(
                status_code=404,
                detail="Report template not found"
            )

    report = Report(
        report_name=report_data.report_name,
        module=report_data.module,
        report_type=report_data.report_type,
        last_run=report_data.last_run,
        owner=report_data.owner,
        status=report_data.status,
        run_time_seconds=report_data.run_time_seconds,
        template_id=report_data.template_id,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get(
    "",
    response_model=list[ReportResponse]
)
def get_reports(
    search: str | None = Query(
        default=None,
        description="Search by report name or owner"
    ),
    module: str | None = Query(default=None),
    report_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    owner: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Report)

    if search:
        search_value = f"%{search}%"

        query = query.filter(
            or_(
                Report.report_name.ilike(search_value),
                Report.owner.ilike(search_value)
            )
        )

    if module:
        query = query.filter(
            Report.module == module
        )

    if report_type:
        if report_type not in ["Scheduled", "On Demand"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid report type"
            )

        query = query.filter(
            Report.report_type == report_type
        )

    if status:
        if status not in [
            "Completed",
            "Failed",
            "Scheduled"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Invalid report status"
            )

        query = query.filter(
            Report.status == status
        )

    if owner:
        query = query.filter(
            Report.owner == owner
        )

    offset = (page - 1) * limit

    reports = (
        query
        .order_by(Report.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return reports


@router.get(
    "/{report_id}",
    response_model=ReportResponse
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report


@router.put(
    "/{report_id}",
    response_model=ReportResponse
)
def update_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    if report_data.template_id is not None:
        template = (
            db.query(ReportTemplate)
            .filter(
                ReportTemplate.id == report_data.template_id
            )
            .first()
        )

        if not template:
            raise HTTPException(
                status_code=404,
                detail="Report template not found"
            )

    update_data = report_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(report, field, value)

    db.commit()
    db.refresh(report)

    return report


@router.delete(
    "/{report_id}"
)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    db.delete(report)
    db.commit()

    return {
        "message": "Report deleted successfully",
        "report_id": report_id
    }