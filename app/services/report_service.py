from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.report import Report


def get_report_summary(db: Session):
    total_reports = (
        db.query(func.count(Report.id))
        .scalar()
        or 0
    )

    completed_reports = (
        db.query(func.count(Report.id))
        .filter(Report.status == "Completed")
        .scalar()
        or 0
    )

    failed_reports = (
        db.query(func.count(Report.id))
        .filter(Report.status == "Failed")
        .scalar()
        or 0
    )

    scheduled_reports = (
        db.query(func.count(Report.id))
        .filter(Report.status == "Scheduled")
        .scalar()
        or 0
    )

    average_run_time = (
        db.query(func.avg(Report.run_time_seconds))
        .filter(Report.run_time_seconds > 0)
        .scalar()
        or 0
    )

    return {
        "total_reports": total_reports,
        "completed_reports": completed_reports,
        "failed_reports": failed_reports,
        "scheduled_reports": scheduled_reports,
        "average_run_time": round(float(average_run_time), 2)
    }


def get_report_type_distribution(db: Session):
    results = (
        db.query(
            Report.report_type,
            func.count(Report.id)
        )
        .group_by(Report.report_type)
        .all()
    )

    return [
        {
            "name": report_type,
            "count": count
        }
        for report_type, count in results
    ]


def get_report_status_distribution(db: Session):
    results = (
        db.query(
            Report.status,
            func.count(Report.id)
        )
        .group_by(Report.status)
        .all()
    )

    return [
        {
            "name": status,
            "count": count
        }
        for status, count in results
    ]