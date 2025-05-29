from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, Enum as SQLEnum
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

class Form(Base):
    __tablename__ = "forms"

    id: Mapped[uuidpk]
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_anonymous: Mapped[bool] = mapped_column(default=False, nullable=False)
    status: Mapped[Status] = mapped_column(SQLEnum(Status, name="status_enum"),nullable=False)

    owner: Mapped["User"] = relationship(back_populates = "forms")
    
