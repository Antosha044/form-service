from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from src.models.enums import Question_type
from src.schemas.choice import ChoiceCreate, ChoiceOut

class QuestionBase(BaseModel):
    text: str = Field(..., example="What is your favorite color?")
    question_type: Question_type = Field(..., example=Question_type.SINGLE_CHOICE)
    order: int = Field(1, ge=1)


class QuestionCreate(QuestionBase):
    form_id: UUID 
    choices: List[ChoiceCreate] | None = None


class QuestionUpdate(BaseModel):
    text: str | None = None
    question_type: Question_type | None = None
    order: int | None = None


class QuestionOut(QuestionBase):
    id: UUID
    form_id: UUID
    choices: List[ChoiceOut] = Field(default_factory=list)

    class Config:
        from_attributes = True