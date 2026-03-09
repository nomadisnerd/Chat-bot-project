from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_messages: int
    messages_by_status: dict[str, int]
    messages_by_channel: dict[str, int]
    total_replies: int
    replies_by_classification: dict[str, int]
