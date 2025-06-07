from pydantic import BaseModel, Field
from uuid import UUID

class ChoiceBase(BaseModel):
    text: str = Field(..., example="Option 1")


class ChoiceCreate(ChoiceBase):
    question_id: UUID  


class ChoiceUpdate(BaseModel):
    text: str | None = None


class ChoiceOut(ChoiceBase):
    id: UUID
    question_id: UUID

    class Config:
        from_attributes = True