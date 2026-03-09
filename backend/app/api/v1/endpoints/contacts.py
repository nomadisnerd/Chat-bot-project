import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import company as company_crud
from app.crud import contact as contact_crud
from app.schemas.contact import ContactCreate, ContactRead, ContactUpdate

router = APIRouter()


def _get_contact_or_404(db: Session, contact_id: uuid.UUID):
    contact = contact_crud.get(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_in: ContactCreate,
    db: Session = Depends(deps.get_db),
) -> ContactRead:
    company = company_crud.get(db, contact_in.company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return contact_crud.create(db, contact_in)


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(
    contact_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> ContactRead:
    return _get_contact_or_404(db, contact_id)


@router.patch("/{contact_id}", response_model=ContactRead)
def patch_contact(
    contact_id: uuid.UUID,
    contact_in: ContactUpdate,
    db: Session = Depends(deps.get_db),
) -> ContactRead:
    db_obj = _get_contact_or_404(db, contact_id)

    update_data = contact_in.model_dump(exclude_unset=True)
    if "company_id" in update_data and update_data["company_id"] is None:
        raise HTTPException(status_code=400, detail="company_id cannot be null")
    company_id = update_data.get("company_id")
    if company_id is not None and company_crud.get(db, company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return contact_crud.update(db, db_obj, contact_in)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Response:
    db_obj = _get_contact_or_404(db, contact_id)
    contact_crud.remove(db, db_obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
