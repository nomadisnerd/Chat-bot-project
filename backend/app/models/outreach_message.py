import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Channel, MessageStatus
from app.db.base_class import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.types import channel_enum, message_status_enum

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
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    rendered_content: Mapped[str] = mapped_column(Text, nullable=False)
    # Legacy column kept for backwards compatibility with old records/migrations.
    message_body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[MessageStatus] = mapped_column(
        message_status_enum,
        nullable=False,
        default=MessageStatus.DRAFTED,
        server_default=MessageStatus.DRAFTED.value,
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

    company: Mapped["Company"] = relationship(back_populates="outreach_messages")
    contact: Mapped["Contact"] = relationship(back_populates="outreach_messages")
    template: Mapped["Template"] = relationship(back_populates="outreach_messages")
    replies: Mapped[list["InboundReply"]] = relationship(
        back_populates="outreach_message",
        cascade="all, delete-orphan",
    )
