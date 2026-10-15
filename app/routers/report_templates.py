from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.database import get_db
from app.models.report_template import ReportTemplate
from app.models.user import User
from app.schemas.report_template import (
    ReportTemplateCreate,
    ReportTemplateResponse,
    ReportTemplateUpdate,
)

router = APIRouter(
    prefix="/api/report-templates",
    tags=["Report Templates"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=ReportTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_template(
    payload: ReportTemplateCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    template = ReportTemplate(**payload.model_dump())
    db.add(template)

    try:
        db.commit()
        db.refresh(template)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A template with this name already exists",
        )

    return template


@router.get("", response_model=list[ReportTemplateResponse])
def list_templates(db: Session = Depends(get_db)):
    return (
        db.query(ReportTemplate)
        .order_by(ReportTemplate.id.desc())
        .all()
    )


@router.get("/{template_id}", response_model=ReportTemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(ReportTemplate).filter(
        ReportTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")

    return template


@router.put("/{template_id}", response_model=ReportTemplateResponse)
def update_template(
    template_id: int,
    payload: ReportTemplateUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    template = db.query(ReportTemplate).filter(
        ReportTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(template, key, value)

    try:
        db.commit()
        db.refresh(template)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A template with this name already exists",
        )

    return template


@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    template = db.query(ReportTemplate).filter(
        ReportTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(template)
    db.commit()

    return {"message": "Template deleted", "template_id": template_id}