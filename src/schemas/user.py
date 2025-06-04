from pydantic import BaseModel, EmailStr, constr
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    
class UserOut(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True


