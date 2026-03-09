import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import Channel


class TemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    channel: Channel
    subject_template: str | None = None
    body_template: str
    is_active: bool = True


class TemplateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    channel: Channel | None = None
    subject_template: str | None = None
    body_template: str | None = None
    is_active: bool | None = None


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    channel: Channel
    subject_template: str | None
    body_template: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
