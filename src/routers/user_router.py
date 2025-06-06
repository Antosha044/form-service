from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.core.jwt_utils import create_access_token
from src.schemas.user import UserOut, UserUpdate
from src.crud import user as user_crud
from src.core.database import get_db
from src.core.dependencies import get_current_user
from src.models.models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: UUID, 
    session: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    user = await user_crud.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=list[UserOut])
async def get_all_users(
    session: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await user_crud.get_all_users(session)

@router.post("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID, 
    user_data: UserUpdate, 
    session: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    updated_user = await user_crud.update_user(user_id, user_data, session)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID, 
    session: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    success = await user_crud.delete_user(user_id, session)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "User deleted successfully"}
