from uuid import uuid4, UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.models.models import User
from src.schemas.user import UserUpdate
from src.schemas.auth import UserRegister
from src.core.security import hash_password

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
   
    
async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.id==user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.email==email))
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def update_user(user_id: UUID, user_data: UserUpdate, session: AsyncSession) -> User | None:
        user = await get_user_by_id(user_id, session)
        if not user:
             return None
        
        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
             update_data["password"] = hash_password(update_data["password"])
        
        for key, value in update_data.items():
             setattr(user, key, value)
        await session.commit()
        return user


async def delete_user(user_id: UUID, session: AsyncSession) -> bool | None:
     user = await get_user_by_id(user_id, session)
     if not user:
          return None
     
     await session.delete(user)
     await session.commit()
     return True


