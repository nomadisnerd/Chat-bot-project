import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    website: str | None = None
    linkedin_url: str | None = None
    industry: str | None = None
    city: str | None = None
    country: str | None = None
    brief: str | None = None
    source: str | None = None


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    website: str | None = None
    linkedin_url: str | None = None
    industry: str | None = None
    city: str | None = None
    country: str | None = None
    brief: str | None = None
    source: str | None = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    website: str | None
    linkedin_url: str | None
    industry: str | None
    city: str | None
    country: str | None
    brief: str | None
    source: str | None
    created_at: datetime
    updated_at: datetime
