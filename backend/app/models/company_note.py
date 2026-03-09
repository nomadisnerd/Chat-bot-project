import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import CompanyNoteType
from app.db.base_class import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.types import company_note_type_enum

if TYPE_CHECKING:
    from app.models.company import Company


class CompanyNote(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "company_notes"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    note_type: Mapped[CompanyNoteType] = mapped_column(company_note_type_enum, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    company: Mapped["Company"] = relationship(back_populates="notes")
