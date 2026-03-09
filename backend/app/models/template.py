from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Channel
from app.db.base_class import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.db.types import channel_enum

if TYPE_CHECKING:
    from app.models.outreach_message import OutreachMessage


class Template(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    channel: Mapped[Channel] = mapped_column(channel_enum, nullable=False)
    subject_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true(),
    )

    messages: Mapped[list["OutreachMessage"]] = relationship(back_populates="template")
