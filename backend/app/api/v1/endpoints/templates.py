import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import template as template_crud
from app.schemas.template import TemplateCreate, TemplateRead, TemplateUpdate

router = APIRouter()


def _get_template_or_404(db: Session, template_id: uuid.UUID):
    template = template_crud.get(db, template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.get("", response_model=list[TemplateRead])
def list_templates(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(deps.get_db),
) -> list[TemplateRead]:
    return template_crud.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=TemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(
    template_in: TemplateCreate,
    db: Session = Depends(deps.get_db),
) -> TemplateRead:
    return template_crud.create(db, template_in)


@router.get("/{template_id}", response_model=TemplateRead)
def get_template(
    template_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> TemplateRead:
    return _get_template_or_404(db, template_id)


@router.patch("/{template_id}", response_model=TemplateRead)
def patch_template(
    template_id: uuid.UUID,
    template_in: TemplateUpdate,
    db: Session = Depends(deps.get_db),
) -> TemplateRead:
    db_obj = _get_template_or_404(db, template_id)
    update_data = template_in.model_dump(exclude_unset=True)
    non_nullable_fields = ("name", "channel", "body_template", "is_active")
    for field in non_nullable_fields:
        if field in update_data and update_data[field] is None:
            raise HTTPException(status_code=400, detail=f"{field} cannot be null")
    return template_crud.update(db, db_obj, template_in)


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Response:
    db_obj = _get_template_or_404(db, template_id)
    template_crud.remove(db, db_obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
