import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ReplyClassification
from app.db.base_class import Base, CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.types import reply_classification_enum

if TYPE_CHECKING:
    from app.models.outreach_message import OutreachMessage


class InboundReply(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "inbound_replies"

    outreach_message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("outreach_messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    classification: Mapped[ReplyClassification | None] = mapped_column(
        reply_classification_enum,
        nullable=True,
    )
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    action_required: Mapped[str | None] = mapped_column(String(255), nullable=True)

    outreach_message: Mapped["OutreachMessage"] = relationship(back_populates="replies")
