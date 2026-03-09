from enum import Enum


class Channel(str, Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"


class OutreachStatus(str, Enum):
    DRAFT = "draft"
    QUEUED = "queued"
    SENT = "sent"
    REPLIED = "replied"
    REJECTED = "rejected"
    POSITIVE = "positive"
    INTERVIEW = "interview"
    NO_RESPONSE = "no_response"
    MANUAL_REVIEW = "manual_review"


class MessageStatus(str, Enum):
    DRAFTED = "drafted"
    SENT = "sent"
    AWAITING_REPLY = "awaiting_reply"
    REPLIED = "replied"
    FOLLOW_UP_DUE = "follow_up_due"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class ReplyClassification(str, Enum):
    REJECTED = "rejected"
    POSITIVE = "positive"
    INTERVIEW = "interview"
    NEUTRAL = "neutral"
    UNCLEAR = "unclear"


class CompanyNoteType(str, Enum):
    MANUAL = "manual"
    AI_BRIEF = "ai_brief"
    FIT_REASON = "fit_reason"
