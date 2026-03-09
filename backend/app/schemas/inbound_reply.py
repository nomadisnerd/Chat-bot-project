import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.enums import ReplyClassification


class InboundReplyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    outreach_message_id: uuid.UUID
    received_at: datetime
    raw_text: str
    summary: str | None
    classification: ReplyClassification | None
    confidence: Decimal | None
    action_required: str | None
    created_at: datetime
