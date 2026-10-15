from sqlalchemy.orm import Session

from app.models.report import Report
from app.repositories.schedule_repository import (
    create_schedule,
    get_schedule,
    list_schedules,
    update_schedule,
)


def add_schedule(db: Session, values: dict):
    report = db.query(Report).filter(
        Report.id == values["report_id"]
    ).first()

    if report is None:
        return None

    return create_schedule(db, values)


def get_schedules(db: Session, report_id: int | None = None):
    return list_schedules(db, report_id)


def edit_schedule(db: Session, schedule_id: int, values: dict):
    schedule = get_schedule(db, schedule_id)

    if schedule is None:
        return None

    return update_schedule(db, schedule, values)


def set_schedule_active(
    db: Session,
    schedule_id: int,
    active: bool,
):
    return edit_schedule(db, schedule_id, {"active": active})