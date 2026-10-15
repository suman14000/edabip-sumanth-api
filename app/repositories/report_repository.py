from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.report import Report
from app.models.report_schedule import ReportSchedule


ALLOWED_SORT_COLUMNS = {
    "id": Report.id,
    "report_name": Report.report_name,
    "module": Report.module,
    "report_type": Report.report_type,
    "status": Report.status,
    "owner": Report.owner,
    "created_at": Report.created_at,
    "last_run": Report.last_run,
}


def list_reports(
    db: Session,
    search: str | None = None,
    module: str | None = None,
    report_type: str | None = None,
    status: str | None = None,
    owner: str | None = None,
    date_from=None,
    date_to=None,
    sort_by: str = "created_at",
    order: str = "desc",
    skip: int = 0,
    limit: int = 20,
):
    query = db.query(Report)

    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Report.report_name.ilike(pattern),
                Report.owner.ilike(pattern),
            )
        )

    if module:
        query = query.filter(Report.module == module)

    if report_type:
        query = query.filter(Report.report_type == report_type)

    if status:
        query = query.filter(Report.status == status)

    if owner:
        query = query.filter(Report.owner == owner)

    if date_from:
        query = query.filter(Report.created_at >= date_from)

    if date_to:
        query = query.filter(Report.created_at <= date_to)

    # Use only a column from the approved mapping.
    sort_column = ALLOWED_SORT_COLUMNS.get(sort_by, Report.created_at)

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.offset(skip).limit(limit).all()


def count_reports(db: Session):
    return db.query(func.count(Report.id)).scalar() or 0


def get_report(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()


def create_report(db: Session, report_data: dict):
    report = Report(**report_data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def update_report(db: Session, report: Report, values: dict):
    for key, value in values.items():
        setattr(report, key, value)

    db.commit()
    db.refresh(report)
    return report


def delete_report(db: Session, report: Report):
    db.delete(report)
    db.commit()


def count_active_schedules(db: Session) -> int:
    return (
        db.query(func.count(ReportSchedule.id))
        .filter(ReportSchedule.active.is_(True))
        .scalar()
        or 0
    )