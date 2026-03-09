import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Channel, OutreachStatus
from app.db.base_class import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.types import channel_enum, outreach_status_enum

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.contact import Contact
    from app.models.inbound_reply import InboundReply
    from app.models.template import Template


class OutreachMessage(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "outreach_messages"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("templates.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    channel: Mapped[Channel] = mapped_column(channel_enum, nullable=False)
    subject: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OutreachStatus] = mapped_column(
        outreach_status_enum,
        nullable=False,
        default=OutreachStatus.DRAFT,
        server_default=OutreachStatus.DRAFT.value,
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_status_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    external_message_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    thread_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_due_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    company: Mapped["Company"] = relationship(back_populates="messages")
    contact: Mapped["Contact"] = relationship(back_populates="messages")
    template: Mapped["Template"] = relationship(back_populates="messages")
    replies: Mapped[list["InboundReply"]] = relationship(
        back_populates="outreach_message",
        cascade="all, delete-orphan",
    )
