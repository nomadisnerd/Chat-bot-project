import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inbound_reply import InboundReply


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[InboundReply]:
    stmt = (
        select(InboundReply)
        .order_by(InboundReply.received_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get(db: Session, reply_id: uuid.UUID) -> InboundReply | None:
    return db.get(InboundReply, reply_id)
