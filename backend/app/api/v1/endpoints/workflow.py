from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.enums import Channel, MessageStatus
from app.crud import company as company_crud
from app.crud import contact as contact_crud
from app.crud import outreach_message as message_crud
from app.crud import template as template_crud
from app.schemas.workflow import CreateOutreachRequest, CreateOutreachResponse
from app.services.template_renderer import render_template

router = APIRouter()


def _resolve_template_body(template_obj) -> str | None:
    for attr in ("body_template", "body", "content"):
        value = getattr(template_obj, attr, None)
        if isinstance(value, str) and value.strip():
            return value
    return None


@router.post(
    "/create-outreach",
    response_model=CreateOutreachResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_outreach(
    payload: CreateOutreachRequest,
    db: Session = Depends(deps.get_db),
) -> CreateOutreachResponse:
    company = company_crud.get(db, payload.company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    contact = None
    if payload.contact_id is not None:
        contact = contact_crud.get(db, payload.contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        if contact.company_id != company.id:
            raise HTTPException(
                status_code=400,
                detail="Contact does not belong to the selected company",
            )

    template = template_crud.get(db, payload.template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")

    template_text = _resolve_template_body(template)
    if template_text is None:
        raise HTTPException(status_code=400, detail="Template text is empty")

    contact_name = contact.full_name if contact and contact.full_name else ""
    render_context = {
        "company_name": company.name,
        "contact_name": contact_name,
        **payload.context,
    }
    rendered_content = render_template(template_text, render_context)

    template_subject = getattr(template, "subject_template", None) or getattr(
        template,
        "subject",
        None,
    )
    request_subject = payload.subject.strip() if payload.subject else ""
    fallback_subject = template_subject.strip() if isinstance(template_subject, str) else ""
    subject = (
        request_subject
        or fallback_subject
        or "Practice / Internship Inquiry"
    )

    channel = payload.channel or getattr(template, "channel", None) or Channel.EMAIL

    follow_up_due_at = datetime.now(timezone.utc) + timedelta(days=payload.follow_up_in_days)

    message = message_crud.create_drafted_outreach(
        db,
        company_id=company.id,
        contact_id=contact.id if contact else None,
        template_id=template.id,
        channel=channel,
        subject=subject,
        rendered_content=rendered_content,
        status=MessageStatus.DRAFTED,
        follow_up_due_at=follow_up_due_at,
    )

    return CreateOutreachResponse(
        message_id=message.id,
        status=message.status,
        subject=message.subject,
        rendered_content=message.rendered_content,
        follow_up_due_at=message.follow_up_due_at,
    )
