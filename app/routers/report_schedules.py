from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.user import User
from app.schemas.report_schedule import (
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
)
from app.services.schedule_service import (
    add_schedule,
    edit_schedule,
    get_schedules,
    set_schedule_active,
)

router = APIRouter(
    prefix="/api/report-schedules",
    tags=["Report Schedules"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_schedule(
    payload: ScheduleCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    schedule = add_schedule(db, payload.model_dump())

    if schedule is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return schedule


@router.get("", response_model=list[ScheduleResponse])
def list_report_schedules(
    report_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_schedules(db, report_id)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_report_schedule(
    schedule_id: int,
    payload: ScheduleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    schedule = edit_schedule(
        db,
        schedule_id,
        payload.model_dump(exclude_unset=True),
    )

    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return schedule


@router.patch("/{schedule_id}/pause", response_model=ScheduleResponse)
def pause_report_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    schedule = set_schedule_active(db, schedule_id, False)

    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return schedule


@router.patch("/{schedule_id}/resume", response_model=ScheduleResponse)
def resume_report_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    schedule = set_schedule_active(db, schedule_id, True)

    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return schedule