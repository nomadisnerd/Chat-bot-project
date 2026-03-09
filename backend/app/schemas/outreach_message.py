import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import Channel, MessageStatus


class OutreachMessageCreate(BaseModel):
    company_id: uuid.UUID
    contact_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    channel: Channel
    subject: str
    rendered_content: str
    status: MessageStatus = MessageStatus.DRAFTED
    sent_at: datetime | None = None
    last_status_at: datetime | None = None
    external_message_id: str | None = None
    thread_id: str | None = None
    follow_up_due_at: datetime | None = None


class OutreachMessageUpdate(BaseModel):
    company_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    channel: Channel | None = None
    subject: str | None = None
    rendered_content: str | None = None
    status: MessageStatus | None = None
    sent_at: datetime | None = None
    last_status_at: datetime | None = None
    external_message_id: str | None = None
    thread_id: str | None = None
    follow_up_due_at: datetime | None = None


class OutreachMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    contact_id: uuid.UUID | None
    template_id: uuid.UUID | None
    channel: Channel
    subject: str
    rendered_content: str
    status: MessageStatus
    sent_at: datetime | None
    last_status_at: datetime | None
    external_message_id: str | None
    thread_id: str | None
    follow_up_due_at: datetime | None
    created_at: datetime
    updated_at: datetime
