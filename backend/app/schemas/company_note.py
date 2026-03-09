import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import CompanyNoteType


class CompanyNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    note_type: CompanyNoteType
    content: str
    created_at: datetime
