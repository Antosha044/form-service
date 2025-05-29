from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base
from src.models.enums import Status, Question_type
from typing import Annotated
import uuid
import datetime


uuidpk = Annotated[uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow
    )]

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    forms: Mapped[list["Form"]] = relationship(back_populates = "owner")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates = "user")

class Form(Base):
    __tablename__ = "forms"

    id: Mapped[uuidpk]
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_anonymous: Mapped[bool] = mapped_column(default=False, nullable=False)
    status: Mapped[Status] = mapped_column(SQLEnum(Status, name="status_enum"), nullable=False)

    owner: Mapped["User"] = relationship(back_populates = "forms")
    questions: Mapped[list["Question"]] = relationship(back_populates = "form", cascade="all, delete-orphan")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates = "form")

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuidpk]
    form_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[Question_type] = mapped_column(SQLEnum(Question_type, name="question_type_enum"), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False, default=1)

    form: Mapped["Form"] = relationship(back_populates="questions")

class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[uuidpk]
    form_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    respondent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    submitted_at: Mapped[created_at]

    form: Mapped["Form"] = relationship(back_populates = "attempts")
    user: Mapped["User"] = relationship(back_populates = "attempts")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[uuidpk]




