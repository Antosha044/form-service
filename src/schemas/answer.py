from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from src.schemas.choice import ChoiceOut


class AnswerBase(BaseModel):
    text: str | None = Field(None, example="Free text answer") 


class AnswerCreate(AnswerBase):
    attempt_id: UUID
    question_id: UUID
    choices_ids: List[UUID] | None = None


class AnswerUpdate(BaseModel):
    text: str | None = None
    choices_ids: List[UUID] | None = None


class AnswerOut(AnswerBase):
    id: UUID
    attempt_id: UUID
    question_id: UUID
    choices: List[ChoiceOut] = Field(default_factory=list)

    class Config:   
        from_attributes = True