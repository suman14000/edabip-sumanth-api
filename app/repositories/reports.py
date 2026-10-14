from datetime import datetime
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.models.report import Report
from app.models.report_schedule import ReportSchedule

ALLOWED_SORT_COLUMNS = {
    "id": Report.id,
    "report_name": Report.report_name,
    "module": Report.module,
    "report_type": Report.report_type,
    "last_run": Report.last_run,
    "owner": Report.owner,
    "status": Report.status,
    "created_at": Report.created_at,
}

def list_reports(db: Session, search: str | None = None, status: str | None = None,
                 module: str | None = None, start_date: datetime | None = None,
                 end_date: datetime | None = None, sort_by: str = "created_at",
                 order: str = "desc", skip: int = 0, limit: int = 100):
    query = db.query(Report)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Report.report_name.ilike(term), Report.owner.ilike(term), Report.module.ilike(term)))
    if status:
        query = query.filter(Report.status == status)
    if module:
        query = query.filter(Report.module == module)
    if start_date:
        query = query.filter(Report.created_at >= start_date)
    if end_date:
        query = query.filter(Report.created_at <= end_date)
    column = ALLOWED_SORT_COLUMNS.get(sort_by)
    if column is None:
        raise ValueError("Unsupported sort_by column")
    query = query.order_by(column.asc() if order == "asc" else column.desc())
    return query.offset(skip).limit(limit).all()

def get_summary(db: Session):
    total = db.query(func.count(Report.id)).scalar() or 0
    completed = db.query(func.count(Report.id)).filter(Report.status == "Completed").scalar() or 0
    failed = db.query(func.count(Report.id)).filter(Report.status == "Failed").scalar() or 0
    scheduled = db.query(func.count(func.distinct(ReportSchedule.report_id))).filter(ReportSchedule.active.is_(True)).scalar() or 0
    average = db.query(func.avg(Report.run_time_seconds)).filter(Report.run_time_seconds > 0).scalar() or 0
    return {"total_reports": total, "completed_reports": completed, "failed_reports": failed,
            "scheduled_reports": scheduled, "average_run_time": round(float(average), 2)}
