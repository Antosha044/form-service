from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.core.jwt_utils import create_access_token
from src.schemas.form import FormCreate, FormUpdate, FormOut
from src.crud import form as form_crud
from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.models.models import Form, User

router = APIRouter(prefix="/forms", tags=["forms"])

@router.post("/", response_model=FormOut)
async def create_form(
    form_data: FormCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    form = await form_crud.create_form(form_data, current_user.id, session)
    return form

@router.get("/me", response_model=list[FormOut])
async def get_forms_by_current_user(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    forms = await form_crud.get_forms_by_user(current_user.id, session)
    return forms

@router.get("/{form_id}", response_model=FormOut)
async def get_form_by_id(
    form_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_db)
):
    form = await form_crud.get_form_by_id(form_id, session)
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")
    return form
