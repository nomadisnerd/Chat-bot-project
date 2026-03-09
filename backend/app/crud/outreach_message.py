import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.outreach_message import OutreachMessage
from app.schemas.outreach_message import OutreachMessageCreate, OutreachMessageUpdate


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[OutreachMessage]:
    stmt = (
        select(OutreachMessage)
        .order_by(OutreachMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get(db: Session, message_id: uuid.UUID) -> OutreachMessage | None:
    return db.get(OutreachMessage, message_id)


def create(db: Session, obj_in: OutreachMessageCreate) -> OutreachMessage:
    db_obj = OutreachMessage(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session,
    db_obj: OutreachMessage,
    obj_in: OutreachMessageUpdate,
) -> OutreachMessage:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: OutreachMessage) -> None:
    db.delete(db_obj)
    db.commit()
