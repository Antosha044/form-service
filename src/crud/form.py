from uuid import uuid4, UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from src.models.models import Form, Question
from src.schemas.form import FormCreate, FormUpdate, FormOut
from src.schemas.auth import UserRegister

async def create_form(form_data: FormCreate, owner_id: UUID, session: AsyncSession) -> Form:
    new_form = Form(
        title = form_data.title,
        description = form_data.description,
        is_anonymous = form_data.is_anonymous,
        status = form_data.status,
        owner_id = owner_id
    )
    session.add(new_form)
    try:
        await session.commit()
        await session.refresh(new_form)
        return new_form
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_form_by_id(form_id: UUID, session: AsyncSession) -> Form | None:
    result = await session.execute(select(Form).options(
        selectinload(Form.questions).selectinload(Question.choices),
        selectinload(Form.attempts)
    ).where(Form.id==form_id))
    form = result.scalar_one_or_none()
    return form


async def get_forms_by_user(user_id: UUID, session: AsyncSession) -> list[Form]:
    result = await session.execute(select(Form).where(Form.owner_id == user_id))
    forms = result.scalars().all()
    return forms



