import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.core.enums import Channel, MessageStatus


class CreateOutreachRequest(BaseModel):
    company_id: uuid.UUID
    contact_id: uuid.UUID | None = None
    template_id: uuid.UUID
    channel: Channel | None = None
    subject: str | None = None
    follow_up_in_days: int = Field(default=7, ge=0, le=90)
    context: dict[str, Any] = Field(default_factory=dict)


class CreateOutreachResponse(BaseModel):
    message_id: uuid.UUID
    status: MessageStatus
    subject: str
    rendered_content: str
    follow_up_due_at: datetime
