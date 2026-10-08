from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report_template import ReportTemplate
from app.schemas.report_template import (
    ReportTemplateCreate,
    ReportTemplateResponse,
    ReportTemplateUpdate,
)


router = APIRouter(
    prefix="/api/report-templates",
    tags=["Report Templates"]
)


@router.post(
    "",
    response_model=ReportTemplateResponse,
    status_code=201
)
def create_template(
    template_data: ReportTemplateCreate,
    db: Session = Depends(get_db)
):
    template = ReportTemplate(
        template_name=template_data.template_name,
        description=template_data.description,
        module=template_data.module,
        created_by=template_data.created_by,
    )

    db.add(template)

    try:
        db.commit()
        db.refresh(template)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Template name already exists"
        )

    return template


@router.get(
    "",
    response_model=list[ReportTemplateResponse]
)
def get_templates(
    db: Session = Depends(get_db)
):
    return (
        db.query(ReportTemplate)
        .order_by(ReportTemplate.id)
        .all()
    )


@router.get(
    "/{template_id}",
    response_model=ReportTemplateResponse
)
def get_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    template = (
        db.query(ReportTemplate)
        .filter(
            ReportTemplate.id == template_id
        )
        .first()
    )

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Report template not found"
        )

    return template


@router.put(
    "/{template_id}",
    response_model=ReportTemplateResponse
)
def update_template(
    template_id: int,
    template_data: ReportTemplateUpdate,
    db: Session = Depends(get_db)
):
    template = (
        db.query(ReportTemplate)
        .filter(
            ReportTemplate.id == template_id
        )
        .first()
    )

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Report template not found"
        )

    update_data = template_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(template, field, value)

    try:
        db.commit()
        db.refresh(template)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Template name already exists"
        )

    return template


@router.delete(
    "/{template_id}"
)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db)
):
    template = (
        db.query(ReportTemplate)
        .filter(
            ReportTemplate.id == template_id
        )
        .first()
    )

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Report template not found"
        )

    db.delete(template)
    db.commit()

    return {
        "message": "Report template deleted successfully",
        "template_id": template_id
    }