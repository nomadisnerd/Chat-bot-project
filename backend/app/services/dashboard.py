from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.inbound_reply import InboundReply
from app.models.outreach_message import OutreachMessage
from app.schemas.dashboard import DashboardStats


def get_dashboard_stats(db: Session) -> DashboardStats:
    total_messages = db.scalar(
        select(func.count()).select_from(OutreachMessage),
    ) or 0
    total_replies = db.scalar(
        select(func.count()).select_from(InboundReply),
    ) or 0

    status_rows = db.execute(
        select(OutreachMessage.status, func.count(OutreachMessage.id)).group_by(
            OutreachMessage.status,
        ),
    ).all()
    channel_rows = db.execute(
        select(OutreachMessage.channel, func.count(OutreachMessage.id)).group_by(
            OutreachMessage.channel,
        ),
    ).all()
    classification_rows = db.execute(
        select(InboundReply.classification, func.count(InboundReply.id)).group_by(
            InboundReply.classification,
        ),
    ).all()

    messages_by_status = {
        (status.value if status is not None else "unknown"): count
        for status, count in status_rows
    }
    messages_by_channel = {
        (channel.value if channel is not None else "unknown"): count
        for channel, count in channel_rows
    }
    replies_by_classification = {
        (classification.value if classification is not None else "unclassified"): count
        for classification, count in classification_rows
    }

    return DashboardStats(
        total_messages=total_messages,
        messages_by_status=messages_by_status,
        messages_by_channel=messages_by_channel,
        total_replies=total_replies,
        replies_by_classification=replies_by_classification,
    )
