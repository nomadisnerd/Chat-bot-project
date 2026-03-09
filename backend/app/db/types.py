from sqlalchemy import Enum as SQLEnum

from app.core.enums import (
    Channel,
    CompanyNoteType,
    MessageStatus,
    OutreachStatus,
    ReplyClassification,
)

channel_enum = SQLEnum(
    Channel,
    name="channel_enum",
    native_enum=False,
    create_constraint=True,
    validate_strings=True,
)

outreach_status_enum = SQLEnum(
    OutreachStatus,
    name="outreach_status_enum",
    native_enum=False,
    create_constraint=True,
    validate_strings=True,
)

message_status_enum = SQLEnum(
    MessageStatus,
    name="message_status_enum",
    native_enum=False,
    create_constraint=True,
    validate_strings=True,
)

reply_classification_enum = SQLEnum(
    ReplyClassification,
    name="reply_classification_enum",
    native_enum=False,
    create_constraint=True,
    validate_strings=True,
)

company_note_type_enum = SQLEnum(
    CompanyNoteType,
    name="company_note_type_enum",
    native_enum=False,
    create_constraint=True,
    validate_strings=True,
)
