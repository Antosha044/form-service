from pydantic import BaseModel, constr
from uuid import UUID
from typing import List
from datetime import datetime
from src.models.enums import Status 
from src.schemas.question import QuestionOut

class FormBase(BaseModel):
    title: constr(min_length=1, max_length=50)
    description: str | None = None
    is_anonymous: bool = False
    status: Status


class FormCreate(FormBase):
    pass


class FormUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_anonymous: bool | None = None
    status: Status | None = None


class FormOut(FormBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    questions: List[QuestionOut]
    
    class Config:
        from_attributes = True
