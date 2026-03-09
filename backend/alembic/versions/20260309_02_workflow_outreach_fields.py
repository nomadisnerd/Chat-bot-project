"""Add workflow-focused outreach message fields and status normalization.

Revision ID: 20260309_02
Revises: 20260309_01
Create Date: 2026-03-09 01:00:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260309_02"
down_revision: str | None = "20260309_01"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def _column_names(bind) -> set[str]:
    return {col["name"] for col in sa.inspect(bind).get_columns("outreach_messages")}


def _drop_status_check_constraints() -> None:
    inspector = sa.inspect(op.get_bind())
    for check in inspector.get_check_constraints("outreach_messages"):
        name = check.get("name")
        sqltext = (check.get("sqltext") or "").lower()
        if name and "status" in sqltext:
            op.drop_constraint(name, "outreach_messages", type_="check")


def upgrade() -> None:
    bind = op.get_bind()
    columns = _column_names(bind)

    if "rendered_content" not in columns:
        op.add_column(
            "outreach_messages",
            sa.Column("rendered_content", sa.Text(), nullable=True),
        )
        columns.add("rendered_content")

    if "status" not in columns:
        op.add_column(
            "outreach_messages",
            sa.Column(
                "status",
                sa.String(length=32),
                nullable=True,
                server_default="drafted",
            ),
        )
        columns.add("status")

    if "sent_at" not in columns:
        op.add_column(
            "outreach_messages",
            sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        )
        columns.add("sent_at")

    if "follow_up_due_at" not in columns:
        op.add_column(
            "outreach_messages",
            sa.Column("follow_up_due_at", sa.DateTime(timezone=True), nullable=True),
        )
        columns.add("follow_up_due_at")

    if "message_body" in columns and "rendered_content" in columns:
        op.execute(
            """
            UPDATE outreach_messages
            SET rendered_content = COALESCE(NULLIF(rendered_content, ''), message_body)
            """
        )

    if "subject" in columns:
        op.execute(
            """
            UPDATE outreach_messages
            SET subject = 'Practice / Internship Inquiry'
            WHERE subject IS NULL OR btrim(subject) = ''
            """
        )
        op.alter_column(
            "outreach_messages",
            "subject",
            existing_type=sa.Text(),
            nullable=False,
        )

    if "rendered_content" in columns:
        op.execute(
            """
            UPDATE outreach_messages
            SET rendered_content = ''
            WHERE rendered_content IS NULL
            """
        )
        op.alter_column(
            "outreach_messages",
            "rendered_content",
            existing_type=sa.Text(),
            nullable=False,
        )

    if "status" in columns:
        op.execute(
            """
            UPDATE outreach_messages
            SET status = CASE status
                WHEN 'draft' THEN 'drafted'
                WHEN 'queued' THEN 'awaiting_reply'
                WHEN 'sent' THEN 'sent'
                WHEN 'replied' THEN 'replied'
                WHEN 'rejected' THEN 'rejected'
                WHEN 'positive' THEN 'accepted'
                WHEN 'interview' THEN 'accepted'
                WHEN 'no_response' THEN 'follow_up_due'
                WHEN 'manual_review' THEN 'awaiting_reply'
                ELSE status
            END
            """
        )

        _drop_status_check_constraints()

        op.execute(
            """
            UPDATE outreach_messages
            SET status = 'drafted'
            WHERE status IS NULL OR status NOT IN (
                'drafted',
                'sent',
                'awaiting_reply',
                'replied',
                'follow_up_due',
                'rejected',
                'accepted'
            )
            """
        )

        op.alter_column(
            "outreach_messages",
            "status",
            existing_type=sa.String(),
            type_=sa.String(length=32),
            nullable=False,
            server_default="drafted",
        )

        check_names = {
            ck.get("name")
            for ck in sa.inspect(bind).get_check_constraints("outreach_messages")
        }
        if "ck_outreach_messages_message_status_enum" not in check_names:
            op.create_check_constraint(
                "ck_outreach_messages_message_status_enum",
                "outreach_messages",
                "status IN ('drafted','sent','awaiting_reply','replied','follow_up_due','rejected','accepted')",
            )


def downgrade() -> None:
    bind = op.get_bind()
    columns = _column_names(bind)

    if "rendered_content" in columns and "message_body" in columns:
        op.execute(
            """
            UPDATE outreach_messages
            SET message_body = COALESCE(message_body, rendered_content)
            """
        )

    if "status" in columns:
        check_names = {
            ck.get("name")
            for ck in sa.inspect(bind).get_check_constraints("outreach_messages")
        }
        if "ck_outreach_messages_message_status_enum" in check_names:
            op.drop_constraint(
                "ck_outreach_messages_message_status_enum",
                "outreach_messages",
                type_="check",
            )

        op.execute(
            """
            UPDATE outreach_messages
            SET status = CASE status
                WHEN 'drafted' THEN 'draft'
                WHEN 'sent' THEN 'sent'
                WHEN 'awaiting_reply' THEN 'queued'
                WHEN 'replied' THEN 'replied'
                WHEN 'follow_up_due' THEN 'no_response'
                WHEN 'rejected' THEN 'rejected'
                WHEN 'accepted' THEN 'positive'
                ELSE status
            END
            """
        )

        op.execute(
            """
            UPDATE outreach_messages
            SET status = 'draft'
            WHERE status IS NULL OR status NOT IN (
                'draft',
                'queued',
                'sent',
                'replied',
                'rejected',
                'positive',
                'interview',
                'no_response',
                'manual_review'
            )
            """
        )

        op.alter_column(
            "outreach_messages",
            "status",
            existing_type=sa.String(),
            type_=sa.String(length=32),
            nullable=False,
            server_default="draft",
        )
        check_names = {
            ck.get("name")
            for ck in sa.inspect(bind).get_check_constraints("outreach_messages")
        }
        if "ck_outreach_messages_outreach_status_enum" not in check_names:
            op.create_check_constraint(
                "ck_outreach_messages_outreach_status_enum",
                "outreach_messages",
                "status IN ('draft','queued','sent','replied','rejected','positive','interview','no_response','manual_review')",
            )

    if "subject" in columns:
        op.alter_column(
            "outreach_messages",
            "subject",
            existing_type=sa.Text(),
            nullable=True,
        )

    if "rendered_content" in columns:
        op.drop_column("outreach_messages", "rendered_content")
