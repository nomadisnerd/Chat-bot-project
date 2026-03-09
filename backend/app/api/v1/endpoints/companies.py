import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import company as company_crud
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.schemas.company_note import CompanyNoteRead
from app.schemas.contact import ContactRead
from app.schemas.outreach_message import OutreachMessageRead

router = APIRouter()


def _get_company_or_404(db: Session, company_id: uuid.UUID):
    company = company_crud.get(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("", response_model=list[CompanyRead])
def list_companies(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(deps.get_db),
) -> list[CompanyRead]:
    return company_crud.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(deps.get_db),
) -> CompanyRead:
    return company_crud.create(db, company_in)


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(
    company_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> CompanyRead:
    return _get_company_or_404(db, company_id)


@router.patch("/{company_id}", response_model=CompanyRead)
def patch_company(
    company_id: uuid.UUID,
    company_in: CompanyUpdate,
    db: Session = Depends(deps.get_db),
) -> CompanyRead:
    db_obj = _get_company_or_404(db, company_id)
    update_data = company_in.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"] is None:
        raise HTTPException(status_code=400, detail="name cannot be null")
    return company_crud.update(db, db_obj, company_in)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> Response:
    db_obj = _get_company_or_404(db, company_id)
    company_crud.remove(db, db_obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{company_id}/contacts", response_model=list[ContactRead])
def list_company_contacts(
    company_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> list[ContactRead]:
    _get_company_or_404(db, company_id)
    return company_crud.get_contacts(db, company_id)


@router.get("/{company_id}/messages", response_model=list[OutreachMessageRead])
def list_company_messages(
    company_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> list[OutreachMessageRead]:
    _get_company_or_404(db, company_id)
    return company_crud.get_messages(db, company_id)


@router.get("/{company_id}/notes", response_model=list[CompanyNoteRead])
def list_company_notes(
    company_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> list[CompanyNoteRead]:
    _get_company_or_404(db, company_id)
    return company_crud.get_notes(db, company_id)
