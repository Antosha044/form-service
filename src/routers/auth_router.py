from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt_utils import create_access_token
from src.schemas.auth import Token, UserRegister, UserLogin
from src.crud import user as user_crud
from src.core.database import get_db
from src.models.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, session: AsyncSession = Depends(get_db)):
    new_user = await user_crud.create_user(session, user_data)

    access_token = create_access_token(data={"sub":str(new_user.id)})
    
    return Token(access_token=access_token)

