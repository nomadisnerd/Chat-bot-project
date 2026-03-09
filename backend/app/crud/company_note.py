import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company_note import CompanyNote


def list_by_company(db: Session, company_id: uuid.UUID) -> list[CompanyNote]:
    stmt = (
        select(CompanyNote)
        .where(CompanyNote.company_id == company_id)
        .order_by(CompanyNote.created_at.desc())
    )
    return list(db.scalars(stmt).all())
