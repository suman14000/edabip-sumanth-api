from sqlalchemy.orm import Session

from app.models.report_activity import ReportActivity


def list_activities(
    db: Session,
    report_id: int | None = None,
    activity_status: str | None = None,
    search: str | None = None,
    date_from=None,
    date_to=None,
    skip: int = 0,
    limit: int = 20,
):
    query = db.query(ReportActivity)

    if report_id is not None:
        query = query.filter(ReportActivity.report_id == report_id)

    if activity_status:
        query = query.filter(
            ReportActivity.activity_status == activity_status
        )

    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(
            ReportActivity.message.ilike(pattern)
        )

    if date_from:
        query = query.filter(ReportActivity.created_at >= date_from)

    if date_to:
        query = query.filter(ReportActivity.created_at <= date_to)

    return (
        query.order_by(ReportActivity.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )