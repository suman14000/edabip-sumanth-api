from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.report import Report
from app.models.report_schedule import ReportSchedule
from app.schemas.report_schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.models.user import User

router = APIRouter(prefix="/api/report-schedules", tags=["Report Schedules"])

@router.post("", response_model=ScheduleResponse, status_code=201)
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not db.query(Report).filter(Report.id == payload.report_id).first():
        raise HTTPException(status_code=404, detail="Report not found")
    row = ReportSchedule(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("", response_model=list[ScheduleResponse])
def list_schedules(active: bool | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(ReportSchedule)
    if active is not None:
        query = query.filter(ReportSchedule.active.is_(active))
    return query.order_by(ReportSchedule.next_run.asc()).all()

@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    row = db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return row

@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, payload: ScheduleUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    row = db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Schedule not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row

@router.patch("/{schedule_id}/pause", response_model=ScheduleResponse)
def pause_schedule(schedule_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    row = db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Schedule not found")
    row.active = False
    db.commit()
    db.refresh(row)
    return row

@router.patch("/{schedule_id}/resume", response_model=ScheduleResponse)
def resume_schedule(schedule_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    row = db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Schedule not found")
    row.active = True
    db.commit()
    db.refresh(row)
    return row

@router.delete("/{schedule_id}", status_code=204)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    row = db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(row)
    db.commit()
    return Response(status_code=204)
