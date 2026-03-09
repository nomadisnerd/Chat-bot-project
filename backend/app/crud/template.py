import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Template]:
    stmt = select(Template).order_by(Template.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get(db: Session, template_id: uuid.UUID) -> Template | None:
    return db.get(Template, template_id)


def create(db: Session, obj_in: TemplateCreate) -> Template:
    db_obj = Template(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Template, obj_in: TemplateUpdate) -> Template:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, db_obj: Template) -> None:
    db.delete(db_obj)
    db.commit()
