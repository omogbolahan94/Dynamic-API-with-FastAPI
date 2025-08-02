from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text, DateTime, Boolean, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(String(50), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_date: Mapped[bool] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

