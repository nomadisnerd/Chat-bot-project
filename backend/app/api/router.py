from fastapi import APIRouter

from app.api.v1.endpoints import companies, contacts, dashboard, messages, replies, templates

api_router = APIRouter()
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(replies.router, prefix="/replies", tags=["replies"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
