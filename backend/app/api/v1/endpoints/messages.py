import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import company as company_crud
from app.crud import contact as contact_crud
from app.crud import outreach_message as message_crud
from app.crud import template as template_crud
from app.schemas.outreach_message import (
    OutreachMessageCreate,
    OutreachMessageRead,
    OutreachMessageUpdate,
)

router = APIRouter()


def _get_message_or_404(db: Session, message_id: uuid.UUID):
    message = message_crud.get(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


def _validate_relations(
    db: Session,
    company_id: uuid.UUID,
    contact_id: uuid.UUID | None,
    template_id: uuid.UUID | None,
) -> None:
    company = company_crud.get(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    if contact_id is not None:
        contact = contact_crud.get(db, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        if contact.company_id != company_id:
            raise HTTPException(
                status_code=400,
                detail="Contact does not belong to the selected company",
            )

    if template_id is not None and template_crud.get(db, template_id) is None:
        raise HTTPException(status_code=404, detail="Template not found")


@router.get("", response_model=list[OutreachMessageRead])
def list_messages(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(deps.get_db),
) -> list[OutreachMessageRead]:
    return message_crud.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=OutreachMessageRead, status_code=status.HTTP_201_CREATED)
def create_message(
    message_in: OutreachMessageCreate,
    db: Session = Depends(deps.get_db),
) -> OutreachMessageRead:
    _validate_relations(
        db,
        company_id=message_in.company_id,
        contact_id=message_in.contact_id,
        template_id=message_in.template_id,
    )
    return message_crud.create(db, message_in)


@router.get("/{message_id}", response_model=OutreachMessageRead)
def get_message(
    message_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> OutreachMessageRead:
    return _get_message_or_404(db, message_id)


@router.patch("/{message_id}", response_model=OutreachMessageRead)
def patch_message(
    message_id: uuid.UUID,
    message_in: OutreachMessageUpdate,
    db: Session = Depends(deps.get_db),
) -> OutreachMessageRead:
    db_obj = _get_message_or_404(db, message_id)

    update_data = message_in.model_dump(exclude_unset=True)

    non_nullable_fields = ("company_id", "channel", "message_body", "status")
    for field in non_nullable_fields:
        if field in update_data and update_data[field] is None:
            raise HTTPException(status_code=400, detail=f"{field} cannot be null")

    company_id = update_data.get("company_id", db_obj.company_id)
    contact_id = update_data.get("contact_id", db_obj.contact_id)
    template_id = update_data.get("template_id", db_obj.template_id)

    _validate_relations(
        db,
        company_id=company_id,
        contact_id=contact_id,
        template_id=template_id,
    )

    return message_crud.update(db, db_obj, message_in)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Response:
    db_obj = _get_message_or_404(db, message_id)
    message_crud.remove(db, db_obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
