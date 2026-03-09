import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def get(db: Session, contact_id: uuid.UUID) -> Contact | None:
    return db.get(Contact, contact_id)


def create(db: Session, obj_in: ContactCreate) -> Contact:
    db_obj = Contact(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Contact, obj_in: ContactUpdate) -> Contact:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Contact) -> None:
    db.delete(db_obj)
    db.commit()


def list_by_company(db: Session, company_id: uuid.UUID) -> list[Contact]:
    stmt = (
        select(Contact)
        .where(Contact.company_id == company_id)
        .order_by(Contact.created_at.desc())
    )
    return list(db.scalars(stmt).all())
