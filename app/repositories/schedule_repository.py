from sqlalchemy.orm import Session

from app.models.report_schedule import ReportSchedule


def list_schedules(db: Session, report_id: int | None = None):
    query = db.query(ReportSchedule)

    if report_id is not None:
        query = query.filter(ReportSchedule.report_id == report_id)

    return query.order_by(ReportSchedule.id.desc()).all()


def get_schedule(db: Session, schedule_id: int):
    return (
        db.query(ReportSchedule)
        .filter(ReportSchedule.id == schedule_id)
        .first()
    )


def create_schedule(db: Session, values: dict):
    schedule = ReportSchedule(**values)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def update_schedule(db: Session, schedule: ReportSchedule, values: dict):
    for key, value in values.items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule