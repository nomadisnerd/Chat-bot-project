import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactCreate(BaseModel):
    company_id: uuid.UUID
    full_name: str | None = None
    role: str | None = None
    email: EmailStr | None = None
    linkedin_profile: str | None = None
    notes: str | None = None


class ContactUpdate(BaseModel):
    company_id: uuid.UUID | None = None
    full_name: str | None = None
    role: str | None = None
    email: EmailStr | None = None
    linkedin_profile: str | None = None
    notes: str | None = None


class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    full_name: str | None
    role: str | None
    email: EmailStr | None
    linkedin_profile: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
