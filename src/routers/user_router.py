from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.core.jwt_utils import create_access_token
from src.schemas.user import UserOut, UserUpdate
from src.crud import user as user_crud
from src.core.database import get_db
from src.models.models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: UUID, session: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


