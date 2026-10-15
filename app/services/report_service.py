from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.report import Report
from app.models.report_schedule import ReportSchedule


def get_report_summary(db: Session):
    total = db.query(func.count(Report.id)).scalar() or 0

    completed = (
        db.query(func.count(Report.id))
        .filter(Report.status == "Completed")
        .scalar()
        or 0
    )

    failed = (
        db.query(func.count(Report.id))
        .filter(Report.status == "Failed")
        .scalar()
        or 0
    )

    # Task 2 requirement: scheduled count is based on active schedules.
    scheduled = (
        db.query(func.count(ReportSchedule.id))
        .filter(ReportSchedule.active.is_(True))
        .scalar()
        or 0
    )

    average = (
        db.query(func.avg(Report.run_time_seconds))
        .filter(Report.run_time_seconds > 0)
        .scalar()
        or 0
    )

    return {
        "total_reports": total,
        "completed_reports": completed,
        "failed_reports": failed,
        "scheduled_reports": scheduled,
        "average_run_time": round(float(average), 2),
    }


def get_report_type_distribution(db: Session):
    results = (
        db.query(Report.report_type, func.count(Report.id))
        .group_by(Report.report_type)
        .all()
    )

    return [
        {"name": report_type, "count": count}
        for report_type, count in results
    ]


def get_report_status_distribution(db: Session):
    results = (
        db.query(Report.status, func.count(Report.id))
        .group_by(Report.status)
        .all()
    )

    return [
        {"name": report_status, "count": count}
        for report_status, count in results
    ]