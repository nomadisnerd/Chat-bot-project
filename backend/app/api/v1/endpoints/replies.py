import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import inbound_reply as reply_crud
from app.schemas.inbound_reply import InboundReplyRead

router = APIRouter()


@router.get("", response_model=list[InboundReplyRead])
def list_replies(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(deps.get_db),
) -> list[InboundReplyRead]:
    return reply_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{reply_id}", response_model=InboundReplyRead)
def get_reply(
    reply_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
) -> InboundReplyRead:
    reply = reply_crud.get(db, reply_id)
    if reply is None:
        raise HTTPException(status_code=404, detail="Reply not found")
    return reply
