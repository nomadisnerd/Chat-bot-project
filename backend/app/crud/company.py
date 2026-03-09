import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.company_note import CompanyNote
from app.models.contact import Contact
from app.models.outreach_message import OutreachMessage
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
    stmt = select(Company).order_by(Company.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get(db: Session, company_id: uuid.UUID) -> Company | None:
    return db.get(Company, company_id)


def create(db: Session, obj_in: CompanyCreate) -> Company:
    db_obj = Company(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Company, obj_in: CompanyUpdate) -> Company:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Company) -> None:
    db.delete(db_obj)
    db.commit()


def get_contacts(db: Session, company_id: uuid.UUID) -> list[Contact]:
    stmt = (
        select(Contact)
        .where(Contact.company_id == company_id)
        .order_by(Contact.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def get_messages(db: Session, company_id: uuid.UUID) -> list[OutreachMessage]:
    stmt = (
        select(OutreachMessage)
        .where(OutreachMessage.company_id == company_id)
        .order_by(OutreachMessage.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def get_notes(db: Session, company_id: uuid.UUID) -> list[CompanyNote]:
    stmt = (
        select(CompanyNote)
        .where(CompanyNote.company_id == company_id)
        .order_by(CompanyNote.created_at.desc())
    )
    return list(db.scalars(stmt).all())
