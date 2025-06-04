from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.models.models import User
from src.schemas.user import UserUpdate
from src.schemas.auth import UserRegister
from uuid import UUID
from sqlalchemy.exc import NoResultFound

def hash_password(password: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

async def create_user(session: AsyncSession, user_data: UserRegister) -> User:
    new_user = User(
        id = uuid4(),
        username = user_data.username,
        email = user_data.email,
        password = hash_password(user_data.password)
    )
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")