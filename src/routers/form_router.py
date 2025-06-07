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