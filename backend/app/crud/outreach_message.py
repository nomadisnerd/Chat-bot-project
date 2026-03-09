import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import Channel, MessageStatus
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
    payload = obj_in.model_dump()
    payload["message_body"] = payload["rendered_content"]
    db_obj = OutreachMessage(**payload)
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
    if "rendered_content" in update_data:
        update_data["message_body"] = update_data["rendered_content"]

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: OutreachMessage) -> None:
    db.delete(db_obj)
    db.commit()


def create_drafted_outreach(
    db: Session,
    *,
    company_id: uuid.UUID,
    contact_id: uuid.UUID | None,
    template_id: uuid.UUID,
    channel: Channel,
    subject: str,
    rendered_content: str,
    status: MessageStatus,
    follow_up_due_at: datetime | None,
) -> OutreachMessage:
    db_obj = OutreachMessage(
        company_id=company_id,
        contact_id=contact_id,
        template_id=template_id,
        channel=channel,
        subject=subject,
        rendered_content=rendered_content,
        message_body=rendered_content,
        status=status,
        follow_up_due_at=follow_up_due_at,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
